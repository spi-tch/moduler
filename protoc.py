import glob
import re

import grpc_tools.protoc
output_path = "moduler/proto"

cli_args = [
    "grpc_tools.protoc",
    "--proto_path=moduler/proto",
    # Python output
    f"--python_out={output_path}",
    f"--grpc_python_out={output_path}",
    # Mypy output
    f"--mypy_out={output_path}",
    f"--mypy_grpc_out={output_path}"
] + glob.glob("moduler/proto/*.proto")


def run():
    code = grpc_tools.protoc.main(cli_args)
    if code:
        raise ValueError(f"{' '.join(cli_args)} finished with exit code {code}")
    # Make pb2 imports in generated scripts relative
    for script in glob.iglob(f"{output_path}/*.py"):
        with open(script, "r+") as file:
            code = file.read()
            file.seek(0)
            file.write(re.sub(r"\n(import .+_pb2.*)", "from . \\1", code))
            file.truncate()


if __name__ == "__main__":
    run()
