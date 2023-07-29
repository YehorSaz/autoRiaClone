import React, {useEffect, useRef, useState} from 'react';
import {socketService} from "./services/socket.service";


const Chat = () => {

    const [socket, setSocket] = useState(null)
    const [messages, setMessages] = useState([])

    const input = useRef()

    useEffect(() => {
        socketInit().then(value => setSocket(value))
    }, [])

    const socketInit = async () => {
        const {chat} = await socketService()
        const client = await chat('all')

        client.onopen = () => {
            console.log('Chat socket connected')
        }
        client.onmessage = (msg) => {
            setMessages(prev => [...prev, JSON.parse(msg.data)])
        }
        return client
    }

    const handlePressEnter = (e) => {
        if (e.key === 'Enter') {
            socket.send(JSON.stringify({
                data: e.target.value,
                action: 'send_message',
                request_id: new Date().getTime()
            }))
            e.target.value = ''
        }
    }

    return (
        <div>
            <div>
                {messages.map(message => <div key={message.id}>{message.user}: {message.message}</div>)}
            </div>
            <input type="text" ref={input} onKeyDown={handlePressEnter}/>
        </div>
    );
};

export {Chat}