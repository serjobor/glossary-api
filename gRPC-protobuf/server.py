from concurrent import futures
import grpc
import glossary_pb2
import glossary_pb2_grpc

TERMS = {
    "gRPC": "Высокопроизводительный RPC поверх HTTP/2.",
    "protobuf": "Формат сериализации данных от Google."
}

class GlossaryServiceServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def CreateTerm(self, request, context):
        TERMS[request.term] = request.definition
        return glossary_pb2.TermEntry(term=request.term, definition=request.definition)

    def GetTerm(self, request, context):
        definition = TERMS.get(request.term)
        if not definition:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Термин не найден")
            return glossary_pb2.TermEntry()
        return glossary_pb2.TermEntry(term=request.term, definition=definition)

    def ListTerms(self, request, context):
        entries = [glossary_pb2.TermEntry(term=k, definition=v) for k, v in TERMS.items()]
        return glossary_pb2.ListTermsResponse(entries=entries)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Glossary server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
