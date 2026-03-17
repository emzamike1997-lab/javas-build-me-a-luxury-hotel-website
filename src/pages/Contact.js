```javascript
import React, { useState } from 'react';

function Contact() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        // Send the form data to the server
        console.log(name, email, message);
    };

    return (
        <main>
            <h1>Get in Touch</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Name:
                    <input type="text" value={name} onChange={(event) => setName(event.target.value)} />
                </label>
                <label>
                    Email:
                    <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
                </label>
                <label>
                    Message:
                    <textarea value={message} onChange={(event) => setMessage(event.target.value)} />
                </label>
                <button type="submit">Send</button>
            </form>
        </main>
    );
}

export default Contact;
```

####