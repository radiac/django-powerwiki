export const addCtrlKeyListener = (char, callbackFn) => {
  window.addEventListener("keydown", e => {
    var key = String.fromCharCode(e.keyCode);
    if ((e.metaKey || e.ctrlKey) && key.toLowerCase() === char) {
      e.preventDefault()
      return callbackFn(e);
    }
    return true;
  });
};
