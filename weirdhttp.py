import enum

class Method(enum.Enum):
    GET = "GET"
    POST = "POST"

class Request:

    @staticmethod
    def parse(data):
        lines = data.split('\r\n')
       
        request = lines[0]
        split = request.split(' ')
       
        # method
        method = split[0]
        assert method in Method.__members__

        # path
        path = split[1]
        assert path.startswith('/')

        # headers
        headers = {}
        for line in lines[1:]:
            if not line:
                break
            split = line.split(': ')
            headers[split[0]] = split[1]

        return Request(method, path, headers)

    def encode(self):
        lines = []
        lines.append(f'{self.method} {self.path} HTTP/1.1')
        for key, value in self.headers.items():
            lines.append(f'{key}: {value}')
        lines.append('')
        return '\r\n'.join(lines)

    def __init__(self, method, path, headers):
        self.method = method
        self.path = path
        self.headers = headers

class Response:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    def encode(self):
        lines = []
        lines.append(f'HTTP/1.1 {self.status}')
        for key, value in self.headers.items():
            lines.append(f'{key}: {value}')
        lines.append('')
        lines.append(self.body)
        return '\r\n'.join(lines)
