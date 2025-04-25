css = """
<style>
body {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f5f7fa;
    padding: 0 20px;
}

.header, .footer {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
    border-radius: 10px;
    margin-bottom: 1.5rem;
    
}

.header > h3 > img {
    height: 70px;
    width: 70px;
    display: "flex";
}

.footer {
    font-size: 1rem;
    font-weight: 300
    margin-top: 2.5rem;
    background: linear-gradient(to right, #3a6073, #16222a);

}

.chat-message {
    padding: 1rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    background-color: #ffffff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    width: 95%;
}

.chat-message.user {
    background-color: #dce3ff;
    border-left: 5px solid #4e72c4;
}

.chat-message.bot {
    background-color: #f1f1f1;
    border-left: 5px solid #5e7a8c;
}

.chat-message .message {
    padding: 0.5rem 1rem;
    color: #333;
    font-size: 1rem;
}

.chat-message.bot .message::before {
    content: '🤖 Bot';
    font-weight: bold;
    display: block;
    color: #5e7a8c;
    font-size: 0.85rem;
}

.chat-message.user .message::before {
    content: '🧑 You';
    font-weight: bold;
    display: block;
    color: #4e72c4;
    font-size: 0.85rem;
}
</style>
"""
