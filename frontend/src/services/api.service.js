import axios from "axios";

const apiService = axios.create({baseURL:'api'});

apiService.interceptors.request.use(config =>{
    const access = localStorage.getItem('access')

    if (access) {
        config.headers.Authorization = `Bearer ${access}`
    }
    return config
})

export {
    apiService
}