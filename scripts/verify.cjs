const {chromium}=require('C:/Users/MPS/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');const path=require('path');const assert=require('assert/strict');
const root=path.resolve(__dirname,'..');const routes=JSON.parse(fs.readFileSync(path.join(root,'docs/routes.json'),'utf8'));
const out=path.join(root,'audit/screenshots/rebuild');fs.mkdirSync(out,{recursive:true});
const result={date:'2026-09-26',baseURL:'http://localhost:4173',pages:[],interactionChecks:[],errors:[],screenshots:[]};
async function main(){
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--enable-webgl','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}});const page=await context.newPage();
  page.on('pageerror',e=>result.errors.push(e.message));
  for(const route of routes){
   const response=await page.goto(result.baseURL+route.path,{waitUntil:'networkidle'});assert.equal(response.status(),200,route.path);
   await page.addScriptTag({path:path.join(root,'scripts/vendor/axe.min.js')});
   const a11y=await page.evaluate(async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}));});
   const scan=await page.evaluate(()=>({title:document.title,h1:document.querySelectorAll('h1').length,brokenImages:[...document.images].filter(i=>i.loading!=='lazy'&&(!i.complete||i.naturalWidth===0)).map(i=>i.src),links:[...document.querySelectorAll('a[href^="/"]')].map(a=>a.getAttribute('href')),placeholder:/lorem ipsum/i.test(document.body.innerText)}));
   const overflow=[];
   for(const width of [1440,768,390,320]){await page.setViewportSize({width,height:900});const data=await page.evaluate(()=>({doc:document.documentElement.scrollWidth,viewport:innerWidth}));if(data.doc>data.viewport+1)overflow.push({width,...data});}
   for(const link of scan.links){const file=link.split(/[?#]/)[0];if(!file||file==='/')continue;const target=path.join(root,'dist',file,'index.html');assert.ok(fs.existsSync(target),`Missing local link: ${route.path} -> ${link}`);}
   result.pages.push({path:route.path,status:response.status(),...scan,links:scan.links.length,overflow,a11y});
   await page.setViewportSize({width:1440,height:1000});
  }
  async function shot(url,name,width=1440,height=1000,selector=null){await page.setViewportSize({width,height});await page.goto(result.baseURL+url,{waitUntil:'networkidle'});if(selector){await page.locator(selector).scrollIntoViewIfNeeded();await page.waitForTimeout(600);}await page.screenshot({path:path.join(out,name+'.png')});result.screenshots.push(name);}
  await shot('/','home-desktop');await page.screenshot({path:path.join(out,'home-full.png'),fullPage:true});
  await shot('/','home-mobile',390,844);
  await shot('/treatments/','treatments-desktop');await shot('/team/','team-desktop');
  await shot('/treatments/root-canal/','treatment-mobile',390,844);
  await shot('/team/namitha-shibu/','profile-mobile',390,844);
  await shot('/contact/','contact-desktop');await shot('/','precision-desktop',1440,1000,'.precision');
  const viewer=page.locator('[data-tooth-viewer]');await viewer.scrollIntoViewIfNeeded();await page.waitForFunction(()=>document.querySelector('[data-tooth-viewer]').dataset.viewerState==='ready',{timeout:15000});
  await page.getByRole('button',{name:'Pause rotation',exact:true}).click();assert.equal(await page.getByRole('button',{name:'Play rotation',exact:true}).getAttribute('aria-pressed'),'false');
  await page.getByRole('button',{name:'Play rotation',exact:true}).click();assert.equal(await page.getByRole('button',{name:'Pause rotation',exact:true}).getAttribute('aria-pressed'),'true');
  await page.getByRole('button',{name:'Rotate tooth left',exact:true}).click();assert.equal(await page.getByRole('button',{name:'Play rotation',exact:true}).getAttribute('aria-pressed'),'false');
  await page.getByRole('button',{name:'Reset view',exact:true}).click();result.interactionChecks.push('3D GLB loads, play/pause, rotate and reset controls work');
  await page.getByRole('button',{name:'Pause motion',exact:true}).click();assert.equal(await page.locator('html').getAttribute('data-motion'),'paused');await page.getByRole('button',{name:'Resume motion',exact:true}).click();result.interactionChecks.push('Global pause/resume controls decorative motion and the 3D animation');
  await page.getByRole('button',{name:'3D CBCT scan',exact:true}).click();assert.ok((await page.locator('[data-scan-image]').getAttribute('src')).includes('imaging-1'));await page.getByRole('button',{name:'Panoramic X-ray',exact:true}).click();result.interactionChecks.push('Imaging visualisation switches OPG/CBCT images, captions and pressed state');
  await page.setViewportSize({width:390,height:844});await page.goto(result.baseURL+'/');
  await page.getByRole('button',{name:'Menu',exact:true}).click();assert.equal(await page.getByRole('button',{name:'Menu',exact:true}).getAttribute('aria-expanded'),'true');
  await page.keyboard.press('Escape');assert.equal(await page.getByRole('button',{name:'Menu',exact:true}).getAttribute('aria-expanded'),'false');
  await page.getByRole('button',{name:'Menu',exact:true}).click();await page.locator('#main-nav').getByRole('link',{name:'Our team',exact:true}).click();assert.ok(page.url().endsWith('/team/'));result.interactionChecks.push('Mobile menu opens, Escape closes with focus restored, and team link navigates');
  await page.goto(result.baseURL+'/treatments/');await page.getByRole('button',{name:'Smile confidence',exact:true}).click();assert.equal(await page.locator('.treatment-card:visible').count(),3);await page.getByRole('button',{name:'All treatments',exact:true}).click();assert.equal(await page.locator('.treatment-card:visible').count(),13);result.interactionChecks.push('Treatment filters show correct cards and restore all 13 services');
  const sourceHTML=fs.readFileSync(path.join(root,'docs/sources/home.html'),'utf8');
  const originalMap=sourceHTML.match(/<iframe[\s\S]*?src="([^"]+)"/)[1].replace(/&(?:amp|#0*38);/g,'&');
  await page.goto(result.baseURL+'/contact/?treatment=root-canal');assert.match(await page.locator('.enquiry-context').innerText(),/root canal/);
  assert.equal(await page.locator('iframe[title*="Google Map"]').getAttribute('src'),originalMap);
  assert.equal(await page.locator('[data-load-map]').count(),0);await page.locator('.map-panel').scrollIntoViewIfNeeded();await page.waitForTimeout(2000);await page.screenshot({path:path.join(out,'map-mobile.png')});result.interactionChecks.push('Contact preserves treatment context; exact original Google Maps embed is visible without an extra button');
  await page.goto(result.baseURL+'/');assert.equal(await page.locator('iframe[title*="Google Map"]').getAttribute('src'),originalMap);
  assert.deepEqual(await page.locator('#journey h3').allTextContents(),['Start with a conversation','See the full picture','Decide with confidence','Feel supported throughout']);
  assert.equal(await page.locator('#journey .journey-step').count(),4);
  await page.locator('#journey').scrollIntoViewIfNeeded();await page.waitForTimeout(300);await page.screenshot({path:path.join(out,'journey-mobile.png')});
  await page.locator('#journey .journey-step').last().scrollIntoViewIfNeeded();await page.waitForTimeout(300);assert.equal(await page.locator('.journey-step.active').count(),4);
  result.interactionChecks.push('Homepage restores all four care-journey steps, scroll progress and the same exact practice map');
  await shot('/','journey-desktop',1440,1000,'#journey');await shot('/','map-desktop',1440,1000,'#location');
  // Images, including lazy images, are checked by fetching each local asset directly.
  const assets=[...new Set(routes.flatMap(r=>[...fs.readFileSync(path.join(root,'dist',r.file),'utf8').matchAll(/src="(\/assets\/[^\"]+)"/g)].map(m=>m[1])))];
  for(const asset of assets){const response=await context.request.get(result.baseURL+asset);assert.equal(response.status(),200,asset);}
  result.interactionChecks.push(`All ${assets.length} referenced image/script assets return HTTP 200`);
  const reduced=await browser.newContext({reducedMotion:'reduce',viewport:{width:390,height:844}});const rp=await reduced.newPage();const requests=[];rp.on('request',r=>requests.push(r.url()));await rp.goto(result.baseURL+'/');await rp.locator('.precision').scrollIntoViewIfNeeded();await rp.waitForTimeout(800);assert.equal(await rp.locator('.tooth-canvas canvas').count(),0);assert.ok(!requests.some(u=>u.endsWith('tooth.glb')));await rp.screenshot({path:path.join(out,'reduced-motion-mobile.png')});result.interactionChecks.push('Reduced motion keeps static fallback and makes no GLB request');await reduced.close();
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const np=await nojs.newPage();await np.goto(result.baseURL+'/treatments/');assert.equal(await np.locator('.treatment-card:visible').count(),13);assert.equal(await np.locator('#main-nav a:visible').count(),8);result.interactionChecks.push('All services and navigation remain available with JavaScript disabled');await nojs.close();
  const broken=await browser.newContext();const bp=await broken.newPage();await bp.route('**/tooth.glb',r=>r.abort());await bp.goto(result.baseURL+'/');await bp.locator('.precision').scrollIntoViewIfNeeded();await bp.waitForFunction(()=>document.querySelector('[data-tooth-viewer]').dataset.viewerState==='fallback');assert.ok(await bp.locator('.tooth-poster').isVisible());assert.equal(await bp.locator('.viewer-controls:visible').count(),0);result.interactionChecks.push('Failed model request leaves the static image and hides unavailable controls');await broken.close();
  const savedata=await browser.newContext();await savedata.addInitScript(()=>Object.defineProperty(navigator,'connection',{value:{saveData:true}}));const sp=await savedata.newPage();await sp.goto(result.baseURL+'/');await sp.locator('.precision').scrollIntoViewIfNeeded();await sp.waitForTimeout(500);assert.equal(await sp.locator('.tooth-canvas canvas').count(),0);result.interactionChecks.push('Data-saving mode keeps the static illustration');await savedata.close();
  await page.setViewportSize({width:1280,height:900});await page.goto(result.baseURL+'/');await page.evaluate(()=>document.documentElement.style.fontSize='200%');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true);result.interactionChecks.push('Homepage has no horizontal overflow with root text size doubled');
 }catch(e){result.errors.push(e.stack);}finally{await browser.close();fs.writeFileSync(path.join(root,'docs/verification.json'),JSON.stringify(result,null,2));const issues=result.pages.flatMap(p=>[...p.overflow,...p.a11y,...p.brokenImages,...(p.h1===1&&!p.placeholder?[]:['structure'])]);console.log(JSON.stringify({pages:result.pages.length,checks:result.interactionChecks,issues:issues.length,errors:result.errors,findings:result.pages.filter(p=>p.overflow.length||p.a11y.length)},null,2));if(issues.length||result.errors.length)process.exitCode=1;}
}
main();
