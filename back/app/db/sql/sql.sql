
CREATE TABLE api.roles (
    id BIGINT PRIMARY KEY IDENTITY(1,1) NOT NULL,

    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(500) NULL,

    created_at DATETIME2(0) NOT NULL DEFAULT GETDATE()

);


CREATE TABLE api.permissions (
    id BIGINT PRIMARY KEY IDENTITY(1,1) NOT NULL,

    name VARCHAR(150) UNIQUE NOT NULL,
    description VARCHAR(500) NULL,

    created_at DATETIME2(0) NOT NULL DEFAULT GETDATE()

);


CREATE TABLE api.user_roles (
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,

    CONSTRAINT PK_user_roles
        PRIMARY KEY (user_id, role_id),

    CONSTRAINT FK_user_roles_user
        FOREIGN KEY (user_id)
        REFERENCES api.users(id),

    CONSTRAINT FK_user_roles_role
        FOREIGN KEY (role_id)
        REFERENCES api.roles(id)
);


CREATE TABLE api.role_permissions (
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,

    CONSTRAINT PK_role_permissions
        PRIMARY KEY (role_id, permission_id),

    CONSTRAINT FK_role_permissions_role
        FOREIGN KEY (role_id)
        REFERENCES api.roles(id),


    CONSTRAINT FK_role_permissions_permission
        FOREIGN KEY (permission_id)
        REFERENCES api.permissions(id)

);