window.onload = () => {
    updateToken = document.getElementById('updateToken')
    updateToken.addEventListener('click', updateTokenAction);

    getData = document.getElementById('getData')
    getData.addEventListener('click', getWigetData);
    
}


async function updateTokenAction() {
    get_user = await query("GET", "/backend_additional/api/user", null, null, true);
    setValueById("oldAdditionalToken", get_user.token)
    newToken = uuid4()
    setValueById("newAdditionalToken", newToken)
    result = await query("POST", "/backend_additional/api/user", {
        "token" : newToken
    }, null, true);
}

async function getWigetData(){
    get_user = await query("GET", "/backend_additional/api/user", null, null, true);
    res = await query("GET", "/backend/api/service", null, {
        "username" : get_user.username,
        "token" : get_user.token
    }, false);
    setValueById("message", res.message)
    newToken = uuid4()
    result = await query("POST", "/backend_additional/api/user", {
        "token" : newToken
    }, null, true);
}

async function query(type, url, data = null, params = null, self = false) {
    req_dict = {
        method: type,
        mode: 'cors',
        cache: 'no-cache',
    }
    
    if (self){
        req_dict["credentials"] = 'include'
    }
    
    if (data){
        req_dict["body"] = JSON.stringify(data)
        req_dict["headers"] = {
            'Content-Type': 'application/json'
        }
        
    }
    if (params){
        url = url + "?" + new URLSearchParams(params)
    }

    const response = await fetch(url, req_dict);
    return await response.json();
}

function uuid4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

async function setValueById(id, value){
    e = document.getElementById(id)
    e.value = value
}

async function getValueById(id) {
    e = document.getElementById(id)
    return e.value
}

