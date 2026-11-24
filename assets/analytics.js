/* Đo lượt xem: không cookie, không IP, không thư viện. */
(function () {
  // >>> CẤU HÌNH: dán Supabase anon (public) key vào đây, KHÔNG dùng service_role. <<<
  // Còn giá trị mặc định thì không gửi gì.
  var SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV4anV5aGJpcXp4aHlrZWppcmtyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTU0NjM3NjksImV4cCI6MjExMTAzOTc2OX0.HsoM8Q2YSPV9zERoKL-8hnpSxYVeoH3Mt_n5sCB-wFE';
  var ENDPOINT = 'https://exjuyhbiqzxhykejirkr.supabase.co/rest/v1/page_views';
  try {
    if (location.protocol === 'file:' || navigator.doNotTrack === '1') return;
    if (!SUPABASE_ANON_KEY || SUPABASE_ANON_KEY.indexOf('PASTE_') === 0) return;
    var body = JSON.stringify({
      path: location.pathname,
      referrer: (document.referrer || '').slice(0, 200),
      ua: (navigator.userAgent || '').slice(0, 180),
      vw: window.innerWidth
    });
    var sent = false;
    if (navigator.sendBeacon) {
      // beacon không đặt được header => apikey qua query
      sent = navigator.sendBeacon(ENDPOINT + '?apikey=' + encodeURIComponent(SUPABASE_ANON_KEY),
        new Blob([body], { type: 'application/json' }));
    }
    if (!sent) {
      fetch(ENDPOINT, {
        method: 'POST',
        keepalive: true,
        headers: {
          'Content-Type': 'application/json',
          'apikey': SUPABASE_ANON_KEY,
          'Authorization': 'Bearer ' + SUPABASE_ANON_KEY,
          'Prefer': 'return=minimal'
        },
        body: body
      }).catch(function () {});
    }
  } catch (e) {}
})();
