import requests

class ZixiBroadcaster:

    def __init__(self, hostname, creds=None, secure=None, port=None):
        base_url_template = "{protocol}://{hostname}:{port}/"
        self.hostname = hostname
        if port is None:
            self.port = "4444"
        else:
            self.port = port
        if creds is None:
            self.creds = ("admin","1234")
        else:
            self.creds = creds
        if secure is None:
            self.protocol = "http"
        elif secure is True:
            self.protocol = "https"
        else:
            self.protocol = "http"
        self.base_url = base_url_template.format(protocol=self.protocol, hostname=self.hostname, port=self.port)
        self.inputs_url = self.base_url + "zixi/streams.json"
        self.outputs_url = self.base_url + "zixi/outputs.json"
        self.reset_input_stats_url_template = self.base_url + "reset_input_stats.json?id={input_id}"
        self.input_stats_url_template = self.base_url + "input_stream_stats.json?id={input_id}"
        self.reset_output_stats_url_template = self.base_url + "reset_output_stream_stats.json?id={output_id}"


    def get_inputs(self):
        inputs_response = requests.get(url=self.inputs_url, auth=self.creds)
        if inputs_response.status_code != requests.codes.ok:
            inputs_response.raise_for_status()
        return inputs_response.json()["streams"]


    def get_all_input_stats(self):
        input_stats = []
        for input in self.get_inputs():
            input_stats_response = requests.get(url=self.input_stats_url_template.format(input_id=input["id"]), auth=self.creds)
            if input_stats_response.status_code != requests.codes.ok:
                input_stats_response.raise_for_status()
            input_stats.append(input_stats_response.json())
        return input_stats


    def reset_input_stats(self, input_id):
        reset_response = requests.get(url=self.reset_input_stats_url_template.format(input_id=input["id"]), auth=self.creds)
        if reset_response.status_code != requests.codes.ok:
            reset_response.raise_for_status()


    def reset_all_input_stats(self):
        for input in self.get_inputs():
            self.reset_input_stats(input_id=input["id"])


    def get_outputs(self, complete=None):
        if complete is None:
            outputs_response = requests.get(url=self.outputs_url, auth=self.creds)
        else:
            outputs_response = requests.get(url=self.outputs_url+"?complete=1", auth=self.creds)
        if outputs_response.status_code != requests.codes.ok:
            outputs_response.raise_for_status()
        return outputs_response.json()["outputs"]


    def reset_output_stats(self, output_id):
        reset_response = requests.get(url=self.reset_output_stats_url_template.format(output_id=output_id), auth=self.creds)
        if reset_response.status_code != requests.codes.ok:
            reset_response.raise_for_status()

       
    def reset_all_output_stats(self):
        for output in self.get_outputs():
            self.reset_output_stats(output_id=output["id"])

