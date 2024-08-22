import grpc
import user_pb2
import user_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        # Create a new user
        create_response = stub.CreateUser(user_pb2.CreateUserRequest(name="John Doe", email="john@example.com"))
        print(f"Created User: {create_response.user}")

        # Get the user
        user_id = create_response.user.id
        get_response = stub.GetUser(user_pb2.GetUserRequest(id=user_id))
        print(f"Retrieved User: {get_response.user}")

        # Update the user
        update_response = stub.UpdateUser(user_pb2.UpdateUserRequest(id=user_id, name="John Smith", email="john.smith@example.com"))
        print(f"Updated User: {update_response.user}")

        # Delete the user
        delete_response = stub.DeleteUser(user_pb2.DeleteUserRequest(id=user_id))
        print(f"Deleted User: {delete_response.success}")

if __name__ == '__main__':
    run()
