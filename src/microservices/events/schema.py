from marshmallow import fields, Schema

class MovieEventSchema(Schema):
    """
    MovieEvent:
      type: object
      properties:
        movie_id:
          type: integer
          description: Идентификатор фильма
          example: 1
        title:
          type: string
          description: Название фильма
          example: "Inception"
        action:
          type: string
          description: Действие с фильмом
          example: "viewed"
        user_id:
          type: integer
          description: Идентификатор пользователя (опционально)
          example: 1
        rating:
          type: number
          format: float
          description: Рейтинг (опционально)
          example: 8.5
        genres:
          type: array
          description: Жанры фильма (опционально)
          items:
            type: string
          example: ["Sci-Fi", "Action"]
        description:
          type: string
          description: Описание фильма (опционально)
          example: "A mind-bending thriller"
      required:
        - movie_id
        - title
        - action
    """
    movie_id = fields.Integer(required=True)
    title = fields.String(required=True)
    action = fields.String(required=True)
    user_id = fields.Integer()
    rating = fields.Float()
    genres = fields.List(fields.String())
    description = fields.String()

class UserEventSchema(Schema):
    """
    UserEvent:
      type: object
      properties:
        user_id:
          type: integer
          description: Идентификатор пользователя
          example: 1
        username:
          type: string
          description: Имя пользователя (опционально)
          example: "john_doe"
        email:
          type: string
          description: Email пользователя (опционально)
          example: "john.doe@example.com"
        action:
          type: string
          description: Действие пользователя
          example: "registered"
        timestamp:
          type: string
          format: date-time
          description: Время события
          example: "2023-01-15T14:30:00Z"
      required:
        - user_id
        - action
        - timestamp
    """
    user_id = fields.Integer(required=True)
    username = fields.String()
    email = fields.String()
    action = fields.String(required=True)
    timestamp = fields.DateTime(required=True)

class PaymentEventSchema(Schema):
    """
    PaymentEvent:
      type: object
      properties:
        payment_id:
          type: integer
          description: Идентификатор платежа
          example: 1
        user_id:
          type: integer
          description: Идентификатор пользователя
          example: 1
        amount:
          type: number
          format: float
          description: Сумма платежа
          example: 9.99
        status:
          type: string
          description: Статус платежа
          example: "completed"
        timestamp:
          type: string
          format: date-time
          description: Время платежа
          example: "2023-01-15T14:30:00Z"
        method_type:
          type: string
          description: Тип метода оплаты (опционально)
          example: "credit_card"
      required:
        - payment_id
        - user_id
        - amount
        - status
        - timestamp
    """
    payment_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    amount = fields.Float(required=True)
    status = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    method_type = fields.String()
