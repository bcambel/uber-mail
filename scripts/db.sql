CREATE DATABASE uber_mailer;

CREATE USER uber_mailer_user WITH SUPERUSER PASSWORD 'uber_mailer_user';

\c uber_mailer;

CREATE TABLE email (id VARCHAR(36),
                    status VARCHAR(10),
                    from_address VARCHAR(100),
                    to_address TEXT,
                    subject TEXT,
                    mail TEXT,
                    created_at TIMESTAMP(6) WITHOUT TIME ZONE,
                    updated_at TIMESTAMP(6) WITHOUT TIME ZONE,
                    result TEXT);
