css = """
<style>
/* Minimal clean styling */
.chat-message {
    padding: 0.8rem;
    border-radius: 6px;
    margin-bottom: 0.6rem;
}
.chat-message.user {
    background: #f5f5f5;
}
.chat-message.bot {
    background: #fff;
    border: 1px solid #eee;
}
.chat-message .message {
    font-size: 0.93rem;
    line-height: 1.6;
}
.chat-message.bot .message::before {
    content: '🤖 AskMyDocs';
    font-weight: 600;
    display: block;
    font-size: 0.78rem;
    margin-bottom: 0.2rem;
    color: #555;
}
.chat-message.user .message::before {
    content: '🧑 You';
    font-weight: 600;
    display: block;
    font-size: 0.78rem;
    margin-bottom: 0.2rem;
    color: #555;
}
.header {
    text-align: center;
    padding: 1rem;
    margin-bottom: 1rem;
}
.header h2 {
    font-size: 1.4rem;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
}
.header h2 img {
    height: 32px;
    width: 32px;
    border-radius: 6px;
}
.header p {
    color: #888;
    font-size: 0.85rem;
    margin-top: 0.2rem;
}
.footer {
    text-align: center;
    font-size: 0.75rem;
    color: #aaa;
    margin-top: 2rem;
    padding: 0.8rem;
}
.footer a {
    color: #888;
    text-decoration: none;
}
</style>
"""
