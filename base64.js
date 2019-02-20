function decode(token) {
  return b64DecodeUnicode(token.split(".", 3)[1]);
}

function b64DecodeUnicode(base64) {
  const urlSafeStr = base64.replace(/_/g, "/").replace(/-/g, "+");
  return decodeURIComponent(
    Array.prototype.map
      .call(atob(urlSafeStr), c => {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );
}
