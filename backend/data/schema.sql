 CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

 CREATE TABLE chat (
     chat_id UUID NOT NULL UNIQUE PRIMARY KEY DEFAULT uuid_generate_v4(),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     ip_addr TEXT,
     mail_send TIMESTAMP
 )

CREATE TABLE message (
    message_id UUID NOT NULL UNIQUE PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_addr TEXT,
    message TEXT,
    read boolean,
    chat_id UUID REFERENCES chat(chat_id)
    -- TODO: Who is the user here? 
)
