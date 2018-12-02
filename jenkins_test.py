import jenkins
import argparse
import sys

class TestJenkins:

    def __init__(self):
        self.params = {}
        self.server = jenkins.Jenkins('http://192.168.71.129:8080', username='admin', password='2b2db67372b84eef822f2d71c85fded7')
        self.parse_fields()
        self.parse_commandline()
        self.build_job()

    def parse_commandline(self):
        parser = argparse.ArgumentParser()
        args, unknown = parser.parse_known_args(sys.argv[1::])
        for name in unknown:
            name = name.replace('--','').split('=')
            if name[0] is 'job_node':
                self.enable_node(name[1])
            else:
                self.params.update({name[0]:name[1]})

    def parse_fields(self):
        file = open('fields.txt','r')
        name = file.readline()
        while(name):
            name = name.strip('\n')
            if name.startswith('[') and name.endswith(']'):
                name = name.strip('[').strip(']')
                value = file.readline()
                if not value:
                    print('File corrupted')
                self.params.update({name:value}) # find by value in braces and send data which in next line
            name = file.readline()

    def enable_node(self,target_node):
        nodes = self.server.get_nodes()
        for node in nodes:
            if not node is target_node:
                self.server.disable_node(node)
            else:
                self.server.enable_node(node)


    def build_job(self):
        try:
            self.server.build_job('GIGA',self.params)
        except jenkins.JenkinsException as e:
            print('Something went wrong '+ str(e))



def main():
    test = TestJenkins()

if __name__ == "__main__": main()
