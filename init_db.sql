ALTER DATABASE bd_lab CHARACTER SET utf8 COLLATE utf8_general_ci;

INSERT INTO core_partytype(name, caption) VALUES
  ('PERSON', 'PERSON'), 
  ('ORGANIZATION', 'ORGANIZATION');

INSERT INTO core_organizationcategory(caption) VALUES 
  ('Кафедра'),
  ('Група');

INSERT INTO core_personcategory(caption) VALUES 
  ('Співробітник'),
  ('Студент');
