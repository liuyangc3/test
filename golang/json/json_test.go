package json


import (
	"testing"
	"strconv"
	"github.com/open-falcon/common/model"
	"fmt"
	"encoding/json"
)

func Test1(t *testing.T) {
	//Max Int64 = 1<<63 -1 =  9223372036854775807
	pvstr := "9223372036854775808"
	prevVersion, err := strconv.ParseInt(pvstr, 10, 64)
	if err != nil {
		prevVersion = -1
		println("error")
	}

	var currentVersion int64 = 100

	if prevVersion > 0 && prevVersion != currentVersion {
		println("return the result")
	} else {
		println("watch self")
	}
}

func Test_Unmarshal(t *testing.T) {

	b := []byte(`[
    {
        "CounterType": "GAUGE",
        "Endpoint": "web-PC",
        "Timestamp": 1487059682,
        "Step": 60,
        "TAGS": "domain=java.lang,type=Threading,name=ThreadCount",
        "Metric": "jvm.java.lang.Threading.ThreadCount",
        "Value": 140
    },
    {
        "CounterType": "GAUGE",
        "Endpoint": "web-PC",
        "Timestamp": 1487059682,
        "Step": 60,
        "TAGS": "domain=java.lang,type=Threading,name=PeakThreadCount",
        "Metric": "jvm.java.lang.Threading.PeakThreadCount",
        "Value": 141
    }]`)
	var metrics []*model.MetricValue
	err := json.Unmarshal(b, &metrics)
	if err != nil {
		//t.Error(err)
		fmt.Printf("err %s, stdout: \n%s\n", err, b)

		fmt.Print("fuck")
	}
	t.Log(metrics)
}



