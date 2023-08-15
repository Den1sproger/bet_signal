CREATE TABLE mail_lists
(
	id serial PRIMARY KEY,
    list_name varchar(255) NOT NULL
);

CREATE TABLE subscribers
(
	id serial PRIMARY KEY,
    nickname varchar(255) NOT NULL,
    chat_id varchar(50) NOT NULL
);

CREATE TABLE bundle
(
	user_id int REFERENCES subscribers(id),
	list_id int REFERENCES mail_lists(id),
    CONSTRAINT user_list_id PRIMARY KEY (user_id, list_id)
)