package rate

import (
	//"golang.org/x/time/rate"
	"testing"
	//"context"
	"time"
	"golang.org/x/time/rate"
)

// put r token in bucket every seconds
// drop new token if bucket size (b) is full
//

// https://github.com/juju/ratelimit/blob/master/ratelimit.go
// https://github.com/uber-go/ratelimit/blob/master/ratelimit.go
// https://github.com/didip/tollbooth/blob/master/limiter/limiter.go
type c struct {
	t time.Duration

}

func TestTimeRateAllow(_ *testing.T) {
	r := rate.Every(time.Second)
	limit := rate.NewLimiter(r, 4)
	for {
		t := time.Now()
		// Allow == AllowN(1)
		if limit.AllowN(t, 1) {
			println("event happen", t.String())
		}
	}
}

