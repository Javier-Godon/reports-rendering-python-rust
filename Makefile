PROTO_DIR := proto
OUT_DIR := app/grpc_client_impl/proto
PROTOC_CMD := python -m grpc_tools.protoc

.PHONY: all clean

all:
	$(PROTOC_CMD) -I$(PROTO_DIR) --proto_path=$(PROTO_DIR) \
		--python_out=$(OUT_DIR) --pyi_out=$(OUT_DIR) --grpc_python_out=$(OUT_DIR) \
		$(PROTO_DIR)/*.proto

clean:
	rm -rf $(OUT_DIR)/*.py $(OUT_DIR)/*.pyi
