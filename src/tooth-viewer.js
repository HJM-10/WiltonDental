import * as THREE from 'three';
import { GLTFLoader } from './vendor/GLTFLoader.js';

export async function mountTooth(root) {
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  if(motion.matches || navigator.connection?.saveData) return;
  const holder = root.querySelector('.tooth-canvas');
  const controls = root.querySelector('.viewer-controls');
  const status = root.querySelector('.viewer-status');
  const auto = root.querySelector('[data-auto]');
  let renderer, model, frame = 0, playing = true, visible = false, disposed = false, last = 0;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35,1,.1,30);
  camera.position.set(0, .5, 5.7); camera.lookAt(0,-.2,0);
  const group = new THREE.Group();scene.add(group); group.rotation.set(.12,-.3,-.1);
  scene.add(new THREE.HemisphereLight(0xe3f4ff,0x526b7d,2.4));
  const key = new THREE.DirectionalLight(0xffffff,4);key.position.set(-3,4,4);scene.add(key);
  const rim = new THREE.DirectionalLight(0x95d9fa,3);rim.position.set(3,1,-2);scene.add(rim);
  const fill = new THREE.DirectionalLight(0xffffff,1);fill.position.set(2,-3,3);scene.add(fill);
  function draw() { if(renderer && !disposed) renderer.render(scene,camera); }
  function halt() { cancelAnimationFrame(frame); frame = 0; }
  function tick(now) {
    frame = 0;
    if(!playing || !visible || document.hidden || disposed || motion.matches || document.documentElement.dataset.motion==='paused') return;
    if(now-last>=32) { group.rotation.y += Math.min((now-last)/1000,.05)*.16; group.position.y=Math.sin(now*.0007)*.035; last=now; draw(); }
    frame=requestAnimationFrame(tick);
  }
  function resume() { halt();last=performance.now();if(playing && visible && !document.hidden && !motion.matches && !disposed && document.documentElement.dataset.motion!=='paused') frame=requestAnimationFrame(tick); }
  function pause() { playing=false;auto.textContent='Play rotation';auto.setAttribute('aria-pressed','false');halt(); }
  function fallback() {
    disposed=true;halt();root.classList.remove('ready');controls.hidden=true;root.dataset.viewerState='fallback';
    status.textContent='Illustrative tooth sculpture. Not a diagnostic scan.';
    if(renderer) renderer.dispose();holder.replaceChildren();
  }
  try {
    renderer=new THREE.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'});
    renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
    renderer.setClearColor(0x102c43,0);renderer.outputColorSpace=THREE.SRGBColorSpace;
    renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1;
    const gltf=await new GLTFLoader().loadAsync('/assets/tooth.glb');
    if(motion.matches) {fallback();return;}
    model=gltf.scene;group.add(model);holder.append(renderer.domElement);
    const resize=() => { if(disposed)return; const {width,height}=holder.getBoundingClientRect();if(!width||!height)return;renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();draw(); };
    const observer=new ResizeObserver(resize);observer.observe(holder);resize();
    root.classList.add('ready');root.dataset.viewerState='ready';controls.hidden=false;auto.textContent='Pause rotation';auto.setAttribute('aria-pressed','true');
    status.textContent='Drag left or right, or use the controls. Illustration, not a diagnostic scan.';
    const intersection=new IntersectionObserver(entries => { visible=entries[0].isIntersecting;resume(); });intersection.observe(root);
    document.addEventListener('visibilitychange',resume);
    document.addEventListener('site-motion',e=>{if(e.detail.paused)pause();else{playing=true;auto.textContent='Pause rotation';auto.setAttribute('aria-pressed','true');resume();}});
    motion.addEventListener('change',() => { if(motion.matches){observer.disconnect();intersection.disconnect();fallback();} });
    renderer.domElement.addEventListener('webglcontextlost',e => {e.preventDefault();observer.disconnect();intersection.disconnect();fallback();});
    let pointer=null, x=0;
    holder.addEventListener('pointerdown',e => { if(disposed || motion.matches)return;pause();pointer=e.pointerId;x=e.clientX;holder.setPointerCapture(pointer); });
    holder.addEventListener('pointermove',e => { if(pointer!==e.pointerId || disposed)return;group.rotation.y+=(e.clientX-x)*.008;x=e.clientX;draw(); });
    const release=() => {pointer=null;};holder.addEventListener('pointerup',release);holder.addEventListener('pointercancel',release);holder.addEventListener('lostpointercapture',release);
    controls.querySelectorAll('[data-rotate]').forEach(button => button.addEventListener('click',()=>{pause();group.rotation.y+=Number(button.dataset.rotate)*Math.PI/8;draw();}));
    root.querySelector('[data-reset]').addEventListener('click',()=>{pause();group.rotation.set(.12,-.3,-.1);draw();});
    auto.addEventListener('click',()=>{playing=!playing;auto.setAttribute('aria-pressed',String(playing));auto.textContent=playing?'Pause rotation':'Play rotation';resume();});
    window.addEventListener('pagehide',()=>{halt();observer.disconnect();intersection.disconnect();renderer.dispose();model.traverse(o=>{if(o.isMesh){o.geometry.dispose();o.material.dispose();}});},{once:true});
  } catch { fallback(); }
}
