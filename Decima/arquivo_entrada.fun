fun fib(n) {
  var res = 0;
  if n < 2 {
    res = 1;
  } else {
    res = fib(n - 1) + fib(n - 2);
  }
  return res;
}

main {
  return fib(6);
}