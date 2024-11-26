import subprocess

def main():

	args = ['tar', '-cvf', 'gridPack.tar','cfgs/',"input/","userfuncs/",'writeDataCards.py','runInterpretation.py','createInputs.py',"tools.py"]
	subprocess.call(args)

main()
