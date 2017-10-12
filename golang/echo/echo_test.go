package echo

import (
	"testing"
	"net/http"
	"github.com/labstack/echo"
	"io/ioutil"
	"time"
	"strconv"

)

func TestRun(t *testing.T) {
	e := echo.New()
	e.GET("/v1/projects/:id", func(c echo.Context) error {
		id, err := strconv.ParseUint(c.Param("id"), 10, 32)
		if err != nil {
			t.Fatalf("ParseUint: %v", err)
		}
		x := uint32(id)

		p := &Project{
			Id:   x,
			Name: "test",
			Repo: Repo{Url:"http://fuck.ocm", Type:"git"},
			Builder: Builder{Language:"go", BuildTool:"go"},
			Created:time.Now(),
		}
		if err := c.Bind(p); err != nil {
			t.Fatalf("Context Bind Project:%v", err)
		}

		return c.JSON(http.StatusOK, p)
	})
	e.Logger.Fatal(e.Start(":1323"))
}

func TestClient(t *testing.T) {
	resp, err := http.Get("http://127.0.0.1:1323/v1/projects/4")
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

func Testhttp(t *testing.T) {

}

type Project struct {
	Id   uint32 `json:"id"`
	Name string `json:"name"`

	Repo    Repo    `json:"repo"`
	Builder Builder `json:"builder"`

	Created  time.Time `json:"created"`
	Modified time.Time `json:"modified"`
}

type Repo struct {
	Url  string `json:"url"`
	Type string `json:"type"` // "git" | "svn"
}

type Builder struct {
	Language  string `json:"language"`  // "java"| "go"| "python"| "c#"
	BuildTool string `json:"buildtool"` // "gradle"| "maven"
}
