from face import face_detect
from gender import gender_predict
from parser import Parser
import sys

if __name__=="__main__":
	login = sys.argv[1]
	password = sys.argv[2]
	
	parser = Parser("https://www.instagram.com", login, password)
	parser.ping()
	if sys.argv[3] == "true":
		depth = int(sys.argv[4])
		print("Parsing Depth: ", depth)
		parser.login()
		parser.parse_followers(sys.argv[5], f"./temp/{sys.argv[6]}.txt", depth)
		parser.parse_accounts(f"./temp/{sys.argv[6]}.txt", f"./dump/{sys.argv[6]}.txt", face_detect, gender_predict)
	else:
		parser.login()
		parser.parse_accounts(f"./temp/{sys.argv[4]}.txt", f"./dump/{sys.argv[4]}.txt", face_detect, gender_predict)
	parser.shut_down(10)
