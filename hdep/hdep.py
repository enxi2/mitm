import re
import os

def response(flow):
  m = re.search(r'.+api/files/videos/(\d{4}/\d{2}/\d{2})/(.+)', flow.request.path)
  if m is not None:
    d = m.group(1).replace("/", "-")
    f = m.group(2).replace("/", "-")
    print(d, f)
    try:
      os.mkdir(d)
    except:
      pass

    fo = open("{}/{}".format(d, f), "wb")
    fo.write(flow.response.content)
    fo.close()
