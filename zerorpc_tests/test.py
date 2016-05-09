import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
for i in range(10):
  print i
  c.hello(str(i))