### 知識點:
1. 此專案為全異步(Async)，建議需先理解python的async/await。
2. 此專案的套件管理是用poetry，建議需先理解poetry。
3. 此專案的db使用PostgreSQL
4. Schemas vs Model
   1. fastapi中的schemas只的是pydantic的class，用來當api的dto。
   2. 這裡的Model指的是ORM的class，此專案的ORM用SQLAlchemy# fastapi-demo
