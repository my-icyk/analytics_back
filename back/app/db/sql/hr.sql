

CREATE TABLE hr.employee_credit (
    id INT IDENTITY(1,1) NOT NULL,
    employee_id BIGINT NOT NULL,
    credit_amount DECIMAL(18,2) NOT NULL,
    nr_months INT NOT NULL,
    start_month DATE NOT NULL,
    status VARCHAR(20) NOT NULL
        CONSTRAINT DF_employee_credit_status DEFAULT ('active'),
    comments NVARCHAR(500) NULL,
    created_at DATETIME2(0) NOT NULL
        CONSTRAINT DF_employee_credit_created_at DEFAULT (SYSDATETIME()),
	paid_off_on DATE NULL,
    created_by BIGINT NOT NULL,
    updated_at DATETIME2(0) NULL,

    CONSTRAINT PK_employee_credit PRIMARY KEY (id),
    CONSTRAINT FK_employee_credit_employee
        FOREIGN KEY (employee_id) REFERENCES dbo.core_employee (id),
    CONSTRAINT FK_employee_credit_created_by
        FOREIGN KEY (created_by) REFERENCES api.users (id),
    CONSTRAINT CK_employee_credit_amount CHECK (credit_amount > 0),
    CONSTRAINT CK_employee_credit_months CHECK (nr_months > 0),
    CONSTRAINT CK_employee_credit_start  CHECK (DAY(start_month) = 1),
    CONSTRAINT CK_employee_credit_status
        CHECK (status IN ('active', 'paid_off', 'cancelled'))
);
GO

CREATE INDEX IX_employee_credit_employee ON hr.employee_credit (employee_id, status);
GO


CREATE TABLE hr.employee_credit_repartition (
    credit_id INT NOT NULL,
    end_of_month DATE NOT NULL,
    remaining_amount DECIMAL(18,2) NOT NULL,

    CONSTRAINT PK_employee_credit_repartition PRIMARY KEY (credit_id, end_of_month),
    CONSTRAINT FK_employee_credit_repartition_credit
        FOREIGN KEY (credit_id) REFERENCES hr.employee_credit (id)
        ON DELETE CASCADE,
    CONSTRAINT CK_employee_credit_repartition_amount CHECK (remaining_amount >= 0)
);
GO

CREATE INDEX IX_employee_credit_repartition_month
    ON hr.employee_credit_repartition (end_of_month)
    INCLUDE (remaining_amount);
GO