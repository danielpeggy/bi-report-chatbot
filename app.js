// Hourly data from Redshift
const H = {
  revByCat: {"10":{"Breakfast":27,"Burgers":373,"Chicken":196,"Desserts":39.5,"Drinks":124.5,"Fries":58.5,"Sides":17.5,"Wraps":36},"11":{"Breakfast":204,"Burgers":2148.5,"Chicken":575.5,"Desserts":226,"Drinks":450.5,"Fries":300.5,"Sides":68.5,"Wraps":72},"12":{"Burgers":4465.5,"Chicken":1381,"Desserts":461.5,"Drinks":861.5,"Fries":658,"Sides":152,"Wraps":236},"13":{"Burgers":4464,"Chicken":1315,"Desserts":530.5,"Drinks":883.5,"Fries":738.5,"Sides":132,"Wraps":160},"14":{"Burgers":4272.5,"Chicken":1459.5,"Desserts":508,"Drinks":936,"Fries":629.5,"Sides":120.5,"Wraps":188},"15":{"Burgers":1742,"Chicken":549.5,"Desserts":193.5,"Drinks":318,"Fries":273,"Sides":75,"Wraps":68},"16":{"Burgers":1707.5,"Chicken":531.5,"Desserts":181.5,"Drinks":333.5,"Fries":280,"Sides":53.5,"Wraps":88},"17":{"Burgers":1739.5,"Chicken":552.5,"Desserts":192.5,"Drinks":304,"Fries":285.5,"Sides":52,"Wraps":68},"18":{"Burgers":3912,"Chicken":1303,"Desserts":474.5,"Drinks":828,"Fries":570.5,"Sides":119.5,"Wraps":164},"19":{"Burgers":4000,"Chicken":1248.5,"Desserts":411,"Drinks":767.5,"Fries":582.5,"Sides":117,"Wraps":208},"20":{"Burgers":3913,"Chicken":1296,"Desserts":395.5,"Drinks":781.5,"Fries":572,"Sides":132,"Wraps":168},"21":{"Burgers":1143.5,"Chicken":381.5,"Desserts":94,"Drinks":233.5,"Fries":196,"Sides":38,"Wraps":20},"22":{"Burgers":1211,"Chicken":253.5,"Desserts":150,"Drinks":225,"Fries":157,"Sides":32.5,"Wraps":44},"23":{"Burgers":1022,"Chicken":446,"Desserts":158.5,"Drinks":189.5,"Fries":208.5,"Sides":20,"Wraps":56}},
  topDishes: {"10":[["Bulgogi Burger",82.5],["Big Mac",76.5],["Angus Third Pounder",71.5],["Quarter Pounder with Cheese",60],["Chicken McCrispy",58.5]],"11":[["Angus Third Pounder",500.5],["Big Mac Combo",450.5],["Bulgogi Burger",363],["Quarter Pounder with Cheese",320],["Big Mac",319.5]],"12":[["Big Mac Combo",994.5],["Angus Third Pounder",793],["Bulgogi Burger",753.5],["Big Mac",724.5],["Quarter Pounder with Cheese",650]],"13":[["Big Mac Combo",1020],["Angus Third Pounder",812.5],["Big Mac",760.5],["Meatball Marinara",665],["Bulgogi Burger",616]],"14":[["Big Mac Combo",909.5],["Angus Third Pounder",825.5],["Big Mac",742.5],["Bulgogi Burger",660],["Quarter Pounder with Cheese",580]],"15":[["Big Mac Combo",459],["Angus Third Pounder",286],["Big Mac",279],["Bulgogi Burger",253],["Meatball Marinara",250]],"16":[["Angus Third Pounder",351],["Bulgogi Burger",341],["Big Mac Combo",314.5],["Big Mac",306],["Meatball Marinara",250]],"17":[["Big Mac",319.5],["Angus Third Pounder",305.5],["Bulgogi Burger",302.5],["Quarter Pounder with Cheese",275],["Big Mac Combo",272]],"18":[["Big Mac Combo",892.5],["Angus Third Pounder",734.5],["Big Mac",616.5],["Bulgogi Burger",588.5],["Quarter Pounder with Cheese",555]],"19":[["Angus Third Pounder",812.5],["Big Mac Combo",722.5],["Big Mac",706.5],["Bulgogi Burger",698.5],["Meatball Marinara",555]],"20":[["Angus Third Pounder",806],["Big Mac Combo",697],["Big Mac",693],["Bulgogi Burger",627],["Meatball Marinara",560]],"21":[["Angus Third Pounder",214.5],["Big Mac Combo",212.5],["Big Mac",207],["Quarter Pounder with Cheese",185],["Meatball Marinara",165]],"22":[["Big Mac Combo",306],["Angus Third Pounder",240.5],["Big Mac",207],["Bulgogi Burger",192.5],["Meatball Marinara",140]],"23":[["Big Mac",207],["Angus Third Pounder",201.5],["Big Mac Combo",170],["Quarter Pounder with Cheese",150],["Bulgogi Burger",148.5]]},
  revByDay: {"10":{"Monday":113,"Tuesday":143,"Wednesday":92.5,"Thursday":138,"Friday":120.5,"Saturday":133.5,"Sunday":131.5},"11":{"Monday":620.5,"Tuesday":519,"Wednesday":475,"Thursday":524.5,"Friday":622.5,"Saturday":614,"Sunday":670},"12":{"Monday":1013,"Tuesday":1073,"Wednesday":1011,"Thursday":1022,"Friday":1394.5,"Saturday":1348.5,"Sunday":1353.5},"13":{"Monday":1036,"Tuesday":1176.5,"Wednesday":1013,"Thursday":1074,"Friday":1295,"Saturday":1298,"Sunday":1331},"14":{"Monday":984.5,"Tuesday":1116.5,"Wednesday":1028.5,"Thursday":1045.5,"Friday":1215,"Saturday":1356,"Sunday":1368},"15":{"Monday":421.5,"Tuesday":366,"Wednesday":377,"Thursday":424.5,"Friday":611.5,"Saturday":438.5,"Sunday":580},"16":{"Monday":360,"Tuesday":404.5,"Wednesday":431,"Thursday":428,"Friday":528,"Saturday":512,"Sunday":512},"17":{"Monday":423.5,"Tuesday":419.5,"Wednesday":393,"Thursday":373,"Friday":564,"Saturday":508.5,"Sunday":512.5},"18":{"Monday":962,"Tuesday":959,"Wednesday":936,"Thursday":1008,"Friday":1239.5,"Saturday":1113,"Sunday":1154},"19":{"Monday":918,"Tuesday":943.5,"Wednesday":895.5,"Thursday":987,"Friday":1094.5,"Saturday":1113,"Sunday":1383},"20":{"Monday":972,"Tuesday":1006,"Wednesday":950,"Thursday":899.5,"Friday":1209,"Saturday":1077.5,"Sunday":1144},"21":{"Monday":331,"Tuesday":248,"Wednesday":260,"Thursday":273,"Friday":280.5,"Saturday":357,"Sunday":357},"22":{"Monday":244,"Tuesday":278,"Wednesday":234.5,"Thursday":258.5,"Friday":256,"Saturday":378.5,"Sunday":423.5},"23":{"Monday":282.5,"Tuesday":265.5,"Wednesday":259,"Thursday":258,"Friday":232,"Saturday":420,"Sunday":383.5}},
  kpi: {"10":{"orders":90,"items":199,"revenue":872},"11":{"orders":398,"items":896,"revenue":4045.5},"12":{"orders":808,"items":1798,"revenue":8215.5},"13":{"orders":808,"items":1804,"revenue":8223.5},"14":{"orders":808,"items":1789,"revenue":8114},"15":{"orders":308,"items":687,"revenue":3219},"16":{"orders":308,"items":686,"revenue":3175.5},"17":{"orders":308,"items":694,"revenue":3194},"18":{"orders":706,"items":1571,"revenue":7371.5},"19":{"orders":706,"items":1575,"revenue":7334.5},"20":{"orders":706,"items":1571,"revenue":7258},"21":{"orders":205,"items":462,"revenue":2106.5},"22":{"orders":205,"items":456,"revenue":2073},"23":{"orders":205,"items":458,"revenue":2100.5}},
  revByMonth: {"10":{"Jan":{"Burgers":100.5,"Drinks":41,"Chicken":95,"Sides":11,"Fries":16.5,"Desserts":6.5,"Breakfast":12.5,"Wraps":20},"Feb":{"Burgers":135,"Chicken":43,"Desserts":10.5,"Fries":26.5,"Breakfast":6.5,"Drinks":29.5,"Wraps":16},"Mar":{"Burgers":137.5,"Chicken":58,"Drinks":54,"Sides":6.5,"Desserts":22.5,"Fries":15.5,"Breakfast":8}},"11":{"Jan":{"Breakfast":84,"Burgers":750,"Chicken":200,"Desserts":65.5,"Drinks":145,"Fries":136.5,"Wraps":40,"Sides":23},"Feb":{"Burgers":762.5,"Chicken":166.5,"Drinks":159.5,"Fries":73,"Breakfast":68,"Desserts":58.5,"Sides":24.5,"Wraps":12},"Mar":{"Burgers":636,"Chicken":209,"Desserts":102,"Drinks":146,"Wraps":20,"Fries":91,"Breakfast":52,"Sides":21}},"12":{"Jan":{"Burgers":1568,"Chicken":539.5,"Desserts":132.5,"Drinks":304.5,"Fries":196.5,"Sides":47.5,"Wraps":104},"Feb":{"Burgers":1405.5,"Chicken":456,"Drinks":308.5,"Fries":235,"Sides":43,"Desserts":103,"Wraps":72},"Mar":{"Burgers":1492,"Desserts":226,"Chicken":385.5,"Drinks":248.5,"Fries":226.5,"Sides":61.5,"Wraps":60}},"13":{"Jan":{"Burgers":1501.5,"Chicken":477,"Desserts":153,"Drinks":350.5,"Fries":301,"Wraps":64,"Sides":48},"Feb":{"Burgers":1507.5,"Desserts":135.5,"Drinks":251.5,"Fries":216,"Chicken":399,"Sides":43.5,"Wraps":52},"Mar":{"Burgers":1455,"Chicken":439,"Desserts":242,"Drinks":281.5,"Fries":221.5,"Wraps":44,"Sides":40.5}},"14":{"Jan":{"Burgers":1539.5,"Chicken":536.5,"Desserts":130,"Drinks":338,"Fries":221.5,"Wraps":68,"Sides":34},"Feb":{"Burgers":1375,"Chicken":494,"Drinks":312,"Fries":217,"Sides":41.5,"Desserts":139.5,"Wraps":44},"Mar":{"Burgers":1358,"Chicken":429,"Desserts":238.5,"Drinks":286,"Fries":191,"Sides":45,"Wraps":76}},"15":{"Jan":{"Burgers":638.5,"Chicken":177,"Desserts":39,"Fries":102.5,"Drinks":112.5,"Wraps":32,"Sides":21.5},"Feb":{"Burgers":479,"Chicken":196.5,"Drinks":91.5,"Fries":94.5,"Desserts":55,"Sides":23,"Wraps":24},"Mar":{"Burgers":624.5,"Chicken":176,"Desserts":99.5,"Drinks":114,"Fries":76,"Sides":30.5,"Wraps":12}},"16":{"Jan":{"Burgers":600,"Desserts":57,"Fries":100,"Wraps":32,"Chicken":183,"Sides":21.5,"Drinks":94.5},"Feb":{"Burgers":635,"Drinks":108,"Fries":106.5,"Wraps":20,"Chicken":165,"Desserts":44.5,"Sides":17.5},"Mar":{"Burgers":472.5,"Chicken":183.5,"Drinks":131,"Desserts":80,"Fries":73.5,"Sides":14.5,"Wraps":36}},"17":{"Jan":{"Burgers":614,"Chicken":213.5,"Desserts":45,"Drinks":95.5,"Fries":106.5,"Sides":22.5,"Wraps":24},"Feb":{"Burgers":625.5,"Chicken":149.5,"Drinks":89.5,"Wraps":28,"Desserts":53,"Fries":87,"Sides":17.5},"Mar":{"Burgers":500,"Chicken":189.5,"Drinks":119,"Fries":92,"Desserts":94.5,"Sides":12,"Wraps":16}},"18":{"Jan":{"Burgers":1443,"Chicken":511,"Desserts":143,"Drinks":292.5,"Fries":208.5,"Sides":39,"Wraps":40},"Feb":{"Burgers":1235,"Chicken":391.5,"Desserts":122,"Drinks":268,"Fries":189.5,"Sides":44.5,"Wraps":68},"Mar":{"Burgers":1234,"Chicken":400.5,"Desserts":209.5,"Drinks":267.5,"Fries":172.5,"Sides":36,"Wraps":56}},"19":{"Jan":{"Burgers":1439.5,"Chicken":459.5,"Desserts":130,"Drinks":284.5,"Wraps":80,"Fries":200,"Sides":40.5},"Feb":{"Burgers":1277,"Chicken":417,"Desserts":105,"Drinks":228.5,"Fries":196.5,"Sides":44,"Wraps":60},"Mar":{"Burgers":1283.5,"Chicken":372,"Desserts":176,"Drinks":254.5,"Fries":186,"Wraps":68,"Sides":32.5}},"20":{"Jan":{"Burgers":1343,"Chicken":440.5,"Desserts":76.5,"Drinks":316.5,"Fries":233.5,"Sides":37,"Wraps":76},"Feb":{"Burgers":1182,"Chicken":362.5,"Drinks":212,"Fries":177,"Desserts":136.5,"Sides":57.5,"Wraps":44},"Mar":{"Burgers":1388,"Chicken":493,"Desserts":182.5,"Drinks":253,"Fries":161.5,"Sides":37.5,"Wraps":48}},"21":{"Jan":{"Burgers":377.5,"Chicken":134.5,"Drinks":83,"Fries":69.5,"Sides":11.5,"Desserts":24.5,"Wraps":12},"Feb":{"Burgers":400.5,"Fries":59,"Chicken":107,"Drinks":76.5,"Wraps":8,"Desserts":18,"Sides":6.5},"Mar":{"Burgers":365.5,"Sides":20,"Chicken":140,"Desserts":51.5,"Fries":67.5,"Drinks":74}},"22":{"Jan":{"Burgers":427.5,"Chicken":102.5,"Desserts":45,"Drinks":66,"Fries":56.5,"Sides":18,"Wraps":20},"Feb":{"Burgers":364,"Chicken":69,"Desserts":46,"Drinks":68.5,"Fries":41.5,"Sides":6,"Wraps":8},"Mar":{"Burgers":419.5,"Chicken":82,"Drinks":90.5,"Fries":59,"Sides":8.5,"Wraps":16,"Desserts":59}},"23":{"Jan":{"Burgers":320.5,"Drinks":93,"Chicken":171.5,"Desserts":36,"Fries":81,"Sides":9,"Wraps":4},"Feb":{"Burgers":392,"Drinks":35,"Chicken":159.5,"Desserts":35.5,"Sides":4,"Fries":55,"Wraps":24},"Mar":{"Burgers":309.5,"Chicken":115,"Desserts":87,"Sides":7,"Fries":72.5,"Drinks":61.5,"Wraps":28}}}
};

const CATS = ['Burgers','Chicken','Drinks','Fries','Desserts','Wraps','Sides','Breakfast'];
const MONTHS = ['Jan','Feb','Mar'];
const DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
const HOURS = [10,11,12,13,14,15,16,17,18,19,20,21,22,23];
const MC = ['#DA291C','#FFC72C','#FF8C00','#C62218','#FFB300','#8B0000','#FF6347','#CD853F'];
const GC = 'rgba(255,255,255,0.06)';

Chart.defaults.color = '#aaa';
Chart.defaults.font.family = "'DM Sans',sans-serif";
Chart.defaults.font.size = 11;

function fmt(v){return 'HK$'+(v>=1000?(v/1000).toFixed(1)+'K':v.toFixed(0));}
function sumObj(objs,key){let t=0;objs.forEach(o=>{if(o&&o[key])t+=o[key]});return t;}
function mergeObjs(objs){let r={};objs.forEach(o=>{if(o)Object.keys(o).forEach(k=>{r[k]=(r[k]||0)+o[k]})});return r;}

let charts = {};
let selectedHour = 'all';

function getData(hour){
  const hrs = hour==='all' ? HOURS : [parseInt(hour)];
  // RevByCat
  const catData = mergeObjs(hrs.map(h=>H.revByCat[h]));
  // RevByMonth
  const monthData = {};
  MONTHS.forEach(m=>{monthData[m]=mergeObjs(hrs.map(h=>H.revByMonth[h]?H.revByMonth[h][m]:null))});
  // TopDishes - aggregate across hours then sort
  const dishMap = {};
  hrs.forEach(h=>{(H.topDishes[h]||[]).forEach(([n,v])=>{dishMap[n]=(dishMap[n]||0)+v})});
  const top5 = Object.entries(dishMap).sort((a,b)=>b[1]-a[1]).slice(0,5);
  // RevByDay
  const dayData = mergeObjs(hrs.map(h=>H.revByDay[h]));
  // KPIs
  let totalOrders=0,totalItems=0,totalRev=0;
  hrs.forEach(h=>{const k=H.kpi[h];if(k){totalOrders+=k.orders;totalItems+=k.items;totalRev+=k.revenue}});
  // OrdersByHour (always show all hours)
  const ordersByHour = HOURS.map(h=>H.kpi[h]?H.kpi[h].orders:0);
  // OrdersByPeriod
  const periods = {Lunch:0,Afternoon:0,Dinner:0,'Late Night':0};
  hrs.forEach(h=>{const o=H.kpi[h]?H.kpi[h].orders:0;if(h>=10&&h<=14)periods.Lunch+=o;else if(h>=15&&h<=17)periods.Afternoon+=o;else if(h>=18&&h<=21)periods.Dinner+=o;else periods['Late Night']+=o});

  return {catData,monthData,top5,dayData,totalOrders,totalItems,totalRev,ordersByHour,periods};
}

function render(hour){
  const d = getData(hour);
  // KPIs
  document.getElementById('kpiSPO').textContent='HK$ '+(d.totalOrders?d.totalRev/d.totalOrders:0).toFixed(2);
  document.getElementById('kpiIPO').textContent=(d.totalOrders?d.totalItems/d.totalOrders:0).toFixed(2);
  document.getElementById('kpiTS').textContent='HK$ '+d.totalRev.toLocaleString();
  document.getElementById('kpiDP').textContent=d.totalItems.toLocaleString();
  document.getElementById('kpiOS').textContent=d.totalOrders.toLocaleString();

  // Destroy old charts
  Object.values(charts).forEach(c=>c.destroy());
  charts = {};

  const bOpts = (hasFmt)=>({responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>fmt(ctx.raw)}}},scales:{y:{grid:{color:GC},ticks:{callback:v=>hasFmt?fmt(v):v}},x:{grid:{display:false},ticks:{maxRotation:45}}}});

  charts.c1 = new Chart(document.getElementById('revByCat'),{type:'bar',data:{labels:CATS,datasets:[{data:CATS.map(c=>d.catData[c]||0),backgroundColor:'#DA291C',borderRadius:4,barPercentage:.7}]},options:bOpts(true)});

  charts.c2 = new Chart(document.getElementById('revByMonth'),{type:'bar',data:{labels:['January','February','March'],datasets:CATS.map((cat,i)=>({label:cat,data:MONTHS.map(m=>d.monthData[m]?d.monthData[m][cat]||0:0),backgroundColor:MC[i],borderRadius:i===0?4:0}))},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{boxWidth:10,padding:8,font:{size:9}}}},scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{color:GC},ticks:{callback:v=>fmt(v)}}}}});

  charts.c3 = new Chart(document.getElementById('topDishes'),{type:'bar',data:{labels:d.top5.map(x=>x[0]),datasets:[{data:d.top5.map(x=>x[1]),backgroundColor:['#DA291C','#FFC72C','#FF8C00','#C62218','#FFB300'],borderRadius:4,barPercentage:.65}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>fmt(ctx.raw)}}},scales:{y:{grid:{color:GC},ticks:{callback:v=>fmt(v)}},x:{grid:{display:false},ticks:{font:{size:9}}}}}});

  charts.c4 = new Chart(document.getElementById('orderByHour'),{type:'line',data:{labels:HOURS,datasets:[{data:d.ordersByHour,borderColor:'#DA291C',backgroundColor:'rgba(218,41,28,0.1)',fill:true,tension:.4,pointRadius:3,pointBackgroundColor:HOURS.map(h=>String(h)===String(hour)?'#FFC72C':'#DA291C'),pointBorderColor:HOURS.map(h=>String(h)===String(hour)?'#FFC72C':'#DA291C'),borderWidth:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{grid:{color:GC}},x:{grid:{display:false}}}}});

  charts.c5 = new Chart(document.getElementById('revByDay'),{type:'line',data:{labels:DAYS,datasets:[{data:DAYS.map(dy=>d.dayData[dy]||0),borderColor:'#DA291C',backgroundColor:'rgba(218,41,28,0.1)',fill:true,tension:.4,pointRadius:3,pointBackgroundColor:'#DA291C',borderWidth:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:ctx=>fmt(ctx.raw)}}},scales:{y:{grid:{color:GC},ticks:{callback:v=>fmt(v)}},x:{grid:{display:false},ticks:{maxRotation:45}}}}});

  const pLabels=Object.keys(d.periods),pVals=Object.values(d.periods);
  charts.c6 = new Chart(document.getElementById('orderByPeriod'),{type:'doughnut',data:{labels:pLabels,datasets:[{data:pVals,backgroundColor:['#DA291C','#FFC72C','#FF8C00','#C62218'],borderWidth:0,hoverOffset:8}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{boxWidth:10,padding:12}}},cutout:'55%'}});
}

// Hour pills
const pillsEl = document.getElementById('hourPills');
const allBtn = document.createElement('button');
allBtn.className = 'hour-pill all-active';
allBtn.textContent = 'All';
allBtn.onclick = ()=>{selectedHour='all';updatePills();render('all')};
pillsEl.appendChild(allBtn);

HOURS.forEach(h=>{
  const btn = document.createElement('button');
  btn.className = 'hour-pill';
  btn.textContent = h;
  btn.onclick = ()=>{selectedHour=h;updatePills();render(h)};
  pillsEl.appendChild(btn);
});

function updatePills(){
  document.querySelectorAll('.hour-pill').forEach(b=>{
    b.classList.remove('active','all-active');
    if(selectedHour==='all'&&b.textContent==='All') b.classList.add('all-active');
    else if(String(selectedHour)===b.textContent) b.classList.add('active');
  });
}

// Initial render
render('all');
