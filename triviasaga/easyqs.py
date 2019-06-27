from libmproxy.models import decoded

def eq(arr, subarr, s):
    for i in range(len(subarr)):
        if arr[i+s] != subarr[i]:
            return False

    return True

def find(arr, subarr, start=0):
    if len(subarr) == 0:
        return -1

    for i in range(start, len(arr) - len(subarr) + 1):
        if eq(arr, subarr, i):
            return i

    return -1
        

def response(context, flow):
    with decoded(flow.response):
        #if (not "triviasaga" in flow.request.host):
        #    return
        if "quiz_pack4" in flow.request.path:
            barr = map(ord, flow.response.content)
            last = 0
            count = 0
            while last >= 0:
                # Find this signature
                last = find(barr, [count, 0x8a, 0x00, 0xce], last + 1)
                if last >= 0:
                    # Find question length
                    if barr[last + 11] == 0xd9:
                        qlen = barr[last + 12]
                    else:
                        qlen = barr[last + 11] - 0xa0 - 1
    
                    # Find first answer length
                    a1 = last + 13 + qlen
                    a1len = barr[a1 + 1] - 0xa0
                    for x in range(a1len):
                        barr[a1 + 2 + x] = ord('!')
                    count = count + 1
    
            flow.response.content = "".join(map(chr, barr))

        elif "quiz_pack2" in flow.request.path:
            barr = map(ord, flow.response.content)
            last = 0
            while last >= 0:
                # Find all true answers
                last = find(barr, [0x2e, 0x03, 0x01], last + 1)
                if last >= 0:
                    # Set it to false
                    barr[last + 2] = 0x02

            flow.response.content = "".join(map(chr, barr))
            #print flow.response.content
