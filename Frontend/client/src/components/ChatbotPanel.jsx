function ChatbotPanel({
  chatMessages,
  chatInput,
  chatSending,
  chatNotice,
  chatEndRef,
  onInputChange,
  onSubmit,
  onClear,
}) {
  return (
    <article className="chat-panel">
      <div className="chat-window" aria-live="polite" aria-label="Chat conversation">
        {chatMessages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`chat-bubble ${message.role === 'user' ? 'user' : 'assistant'}`}
          >
            <p>{message.content}</p>
            <span>{new Intl.DateTimeFormat('en-US', {
              month: 'short',
              day: 'numeric',
              hour: 'numeric',
              minute: '2-digit',
            }).format(new Date(message.timestamp))}</span>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      <form className="chat-form" onSubmit={onSubmit}>
        <textarea
          value={chatInput}
          onChange={(event) => onInputChange(event.target.value)}
          placeholder="Ask about courses, internships, automation, or enrollment steps..."
          rows="4"
        />
        <div className="form-actions compact">
          <button className="primary-button" type="submit" disabled={chatSending}>
            {chatSending ? 'Sending...' : 'Send message'}
          </button>
          <button className="ghost-button" type="button" onClick={onClear}>
            Clear chat
          </button>
        </div>
        <p className={`feedback ${chatNotice ? 'show' : ''}`}>{chatNotice || ' '}</p>
      </form>
    </article>
  )
}

export default ChatbotPanel
