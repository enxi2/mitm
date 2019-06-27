def request(flow):
    newHash = "321187995bc7cdc2b5fc91b11a96e2baa8602c62"
    if flow.request.urlencoded_form is not None and flow.request.urlencoded_form.get("app", "") == "com.nianticlabs.pokemongo":
        if flow.request.path == "/auth":
            print("Modifying sig")
            flow.request.urlencoded_form["callerSig"] = newHash
            flow.request.urlencoded_form["client_sig"] = newHash
        elif flow.request.path == "/c2dm/register3":
            print("Modifying cert")
            flow.request.urlencoded_form["cert"] = newHash

