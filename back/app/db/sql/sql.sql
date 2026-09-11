CREATE TABLE api.roles (
    id BIGINT PRIMARY KEY IDENTITY(1,1) NOT NULL,

    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(500) NULL,

    created_at DATETIME2(0) NOT NULL DEFAULT GETDATE()

);


CREATE TABLE api.permissions (
    id BIGINT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    name VARCHAR(150) UNIQUE NOT NULL

);


CREATE TABLE api.user_roles (
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,

    CONSTRAINT PK_user_roles
        PRIMARY KEY (user_id, role_id),

    CONSTRAINT FK_user_roles_user
        FOREIGN KEY (user_id)
        REFERENCES api.users(id)
		ON DELETE CASCADE,

    CONSTRAINT FK_user_roles_role
        FOREIGN KEY (role_id)
        REFERENCES api.roles(id)
		ON DELETE CASCADE
);


CREATE TABLE api.role_permissions (
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,

    CONSTRAINT PK_role_permissions
    PRIMARY KEY (role_id, permission_id),

    CONSTRAINT FK_role_permissions_role
    FOREIGN KEY (role_id)
	REFERENCES api.roles(id)
	ON DELETE CASCADE,


    CONSTRAINT FK_role_permissions_permission
    FOREIGN KEY (permission_id)
    REFERENCES api.permissions(id)
	ON DELETE CASCADE
);

CREATE TABLE api.refresh_tokens (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES api.users(id),
    token_hash VARCHAR(64) NOT NULL UNIQUE,
    expires_at DATETIME2 NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    revoked_at DATETIME2 NULL,
    replaced_by BIGINT NULL REFERENCES api.refresh_tokens(id)
);