CREATE TABLE api.user_sessions (
    session_id BIGINT IDENTITY(1,1) NOT NULL,
    user_id BIGINT NOT NULL,
    token_hash CHAR(64) NOT NULL,
    created_at DATETIME2(6) NOT NULL CONSTRAINT DF_user_sessions_created DEFAULT SYSUTCDATETIME(),
    expires_at DATETIME2(6) NOT NULL,

    CONSTRAINT PK_user_sessions PRIMARY KEY (session_id),
    CONSTRAINT UQ_user_sessions_token_hash UNIQUE (token_hash),
    CONSTRAINT FK_user_sessions_user FOREIGN KEY (user_id)
        REFERENCES api.users(id) ON DELETE CASCADE,
    CONSTRAINT CK_user_sessions_expiry CHECK (expires_at > created_at)
);

CREATE INDEX IX_user_sessions_user_id ON api.user_sessions (user_id);
CREATE INDEX IX_user_sessions_expires_at ON api.user_sessions (expires_at);