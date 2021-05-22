async function updateTokenAction() {
    get_user = await query("GET", "/backend_additional/api/user", null, null, true);
    setValueById("oldAdditionalToken", get_user.token)
    newToken = uuid4()
    setValueById("newAdditionalToken", newToken)
    result = query("POST", "/backend_additional/api/user", {
        "token" : newToken
    }, null, true);
}

async function getWigetData(){
    res = await query("GET", "/backend/api/user", null, null, false);
    console.log(res)
}

async function query(type, url, data = null, params = null, self = false) {
    req_dict = {
        method: type,
        mode: 'cors',
        cache: 'no-cache',
    }
    
    if (!self){
        url = "http://127.0.0.1:5000" + url
    } else {
        req_dict["credentials"] = 'include'
    }
    
    if (data){
        req_dict["body"] = JSON.stringify(data)
        req_dict["headers"] = {
            'Content-Type': 'application/json'
        }
    }
    // if (params){
    //     Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    // }
    const response = await fetch(url, req_dict);
    return await response.json();
}