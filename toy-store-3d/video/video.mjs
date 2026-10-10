import {chromium} from 'playwright-core';
import fs from 'fs';
const fps=+process.argv[2]||25, only=process.argv[3];
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args:['--use-gl=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('http://localhost:8765/anim.html');await p.waitForFunction('window.READY===true',null,{timeout:180000});
const dur=await p.evaluate('window.DURATION');console.log('duration',dur);
fs.mkdirSync('frames',{recursive:true});
const WT=await p.evaluate('window.WT');const start=process.argv[4]?Math.floor(WT[+process.argv[4]]*fps):0;console.log('start',start);const n=only?1:Math.ceil(dur*fps);const t0=Date.now();
for(let i=only?0:start;i<n;i++){const tt=only?+only:i/fps;const url=await p.evaluate(`window.frame(${tt})`);
 fs.writeFileSync(`frames/${only?'test':String(i).padStart(5,'0')}.jpg`,Buffer.from(url.split(',')[1],'base64'));
 if(i%100==0)console.log(i,n,((Date.now()-t0)/1000).toFixed(0)+'s');}
await b.close();
