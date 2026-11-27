const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const dir=process.argv[2];const scale=+process.argv[3];
for(const v of ['grunge','clean']){const p=await b.newPage({viewport:{width:1200,height:1800},deviceScaleFactor:scale});
await p.goto('file://'+dir+'/'+(process.argv[4]||'poster.html')+'#'+v);await p.waitForSelector('body[data-ready]').catch(()=>{});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.locator('#p').screenshot({path:dir+'/'+(process.argv[5]||'out')+'-'+v+'-x'+scale+'.png'});await p.close();}
await b.close();})();
