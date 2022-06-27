from google.protobuf import text_format
from proto import tournament_pb2


def read_tournament():
    # TODO: Implement reading a tournament from the SQLite3 db.
    tournament = None
    return dict(tournament)
    pass


def initiate_tournament(tournament_filename: str):
    tournament_file = open(tournament_filename, 'r')
    tournament_textproto = tournament_file.read()
    tournament_proto = text_format.Parse(tournament_textproto, tournament_pb2.Tournament())
    
    print(tournament_proto)

    tournament_file.close()

if __name__ == '__main__':
    initiate_tournament('../testdata/test_tournament.textproto')
