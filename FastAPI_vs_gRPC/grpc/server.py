from concurrent import futures
import logging
import grpc

import glossary_pb2
import glossary_pb2_grpc

class TermsService(glossary_pb2_grpc.TermsServiceServicer):
  def __init__(self):
    self.data = {
      'fps': glossary_pb2.Term(
        title='fps',
        definition='Количество сменяемых на интерфейсе кадров за одну секунду.',
        source_link='https://developer.mozilla.org/ru/docs/Glossary/FPS'
      ),
      'fcp': glossary_pb2.Term(
        title='fcp',
        definition='Время, за которое пользователь увидит какое-то содержимое веб-страницы, например, текст или картинку.',
        source_link='https://developer.mozilla.org/ru/docs/Glossary/First_contentful_paint'
      ),
      'fid': glossary_pb2.Term(
        title='fid',
        definition='Время ожидания до первого взаимодействия с контентом.',
        source_link='https://habr.com/ru/companies/timeweb/articles/714280/'
      ),
      'tbt': glossary_pb2.Term(
        title='tbt',
        definition='Общее количество времени, когда основной поток заблокирован достаточно долго, чтобы реагировать на взаимодействия пользователя.',
        source_link='https://habr.com/ru/companies/domclick/articles/549098/'
      ),
      'cls': glossary_pb2.Term(
        title='cls',
        definition='Какое количество содержимого во viewport двигалось во время загрузки страницы.',
        source_link='https://habr.com/ru/companies/domclick/articles/549098/'
      ),
    }

  def GetAllTerms(self, request, context):
    """Получить список всех терминов"""
    return glossary_pb2.TermList(terms=self.data)

  def CreateTerm(self, request, context):
    """Добавить новый термин с описанием"""
    keyword = request.keyword
    term = request.term
    
    if keyword in self.data:
      context.set_code(grpc.StatusCode.ALREADY_EXISTS)
      context.set_details(f"Термин '{keyword}' уже существует")
      return glossary_pb2.Term()
    
    self.data[keyword] = term
    return term

  def UpdateTerm(self, request, context):
    """Обновить существующий термин"""
    keyword = request.keyword
    term_update = request.term_update
    
    if keyword not in self.data:
      context.set_code(grpc.StatusCode.NOT_FOUND)
      context.set_details(f"Термин '{keyword}' не найден")
      return glossary_pb2.Term()
    
    if term_update.definition:
      self.data[keyword].definition = term_update.definition
    if term_update.source_link:
      self.data[keyword].source_link = term_update.source_link
    
    return self.data[keyword]

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  glossary_pb2_grpc.add_TermsServiceServicer_to_server(TermsService(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  print("Terms Server started on port 50051")
  server.wait_for_termination()

if __name__ == '__main__':
  logging.basicConfig()
  serve()