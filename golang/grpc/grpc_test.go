package grpc

import (
	"testing"
	"net"
	"google.golang.org/grpc"
	"golang.org/x/net/context"
	"google.golang.org/grpc/reflection"

	"github.com/grpc-ecosystem/grpc-gateway/runtime"
	pb "github.com/liuyangc3/golangtest/grpc/proto"
	"net/http"
	"io/ioutil"
	"fmt"
)

type server struct{}

func (s server) GetProject(ctx context.Context, in *pb.GetProjectRequest) (*pb.ProjectMessage, error) {
	return &pb.ProjectMessage{Id: in.Id, Name: "fuck"}, nil
}

const port = ":9090"

func TestRpcServer(t *testing.T) {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		t.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterProjectServiceServer(s, &server{})
	// Register reflection service on gRPC server.
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		t.Fatalf("failed to serve: %v", err)
	}
}

func TestRpcClient(t *testing.T) {
	address := fmt.Sprintf("localhost%s", port)

	// Set up a connection to the server.
	conn, err := grpc.Dial(address, grpc.WithInsecure())
	if err != nil {
		t.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewProjectServiceClient(conn)

	// Contact the server and print out its response.
	r, err := c.GetProject(context.Background(), &pb.GetProjectRequest{Id: "1"})
	if err != nil {
		t.Fatalf("could not GetProject: %v", err)
	}
	t.Logf("from service id->%s, name->%s", r.Id, r.Name)
}

func TestHttpServer(t *testing.T) {
	address := fmt.Sprintf("localhost%s", port)
	//projectEndpoint := flag.String("project_endpoint", "localhost:9090", "endpoint of ProjectService")
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithInsecure()}
	err := pb.RegisterProjectServiceHandlerFromEndpoint(
		context.Background(), mux, address, opts)
	if err != nil {
		t.Fatalf("failed to RegisterProjectService: %v", err)
	}

	err = http.ListenAndServe(":8080", mux)
	if err != nil {
		t.Fatalf("ListenAndServe error: %v", err)
	}
}

func TestHttpClient(t *testing.T) {
	resp, err := http.Get("http://127.0.0.1:8080/v1/projects/4")
	if err != nil {
		t.Fatalf("client get error: %v", err)
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatalf("read body error: %v", err)
	}

	t.Log(string(body))
}
