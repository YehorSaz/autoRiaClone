import {w3cwebsocket as W3cWebsocket} from "websocket"
import {apiService} from "./api.service";

const baseURL = 'ws://localhost/api'

const socketService = async () => {
    const {data:{token}} = await apiService.get('/auth/socket_token')
    return {
        chat: async (room) => new W3cWebsocket(`${baseURL}/chat/${room}?token=${token}`),
        cars: async () => new W3cWebsocket(`${baseURL}/cars?token=${token}`)
    }
}

export {
    socketService
}