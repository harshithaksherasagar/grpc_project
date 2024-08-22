from concurrent import futures
import grpc
import user_pb2
import user_pb2_grpc
import uuid

# In-memory database for simplicity
users_db = {}

class UserService(user_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        user_id = str(uuid.uuid4())
        user = user_pb2.User(id=user_id, name=request.name, email=request.email)
        users_db[user_id] = user
        return user_pb2.UserResponse(user=user)

    def GetUser(self, request, context):
        user = users_db.get(request.id)
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        return user_pb2.UserResponse(user=user)

    def UpdateUser(self, request, context):
        user = users_db.get(request.id)
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        user.name = request.name
        user.email = request.email
        users_db[request.id] = user
        return user_pb2.UserResponse(user=user)

    def DeleteUser(self, request, context):
        if request.id in users_db:
            del users_db[request.id]
            return user_pb2.DeleteResponse(success=True)
        else:
            return user_pb2.DeleteResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
