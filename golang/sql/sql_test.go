package sql

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"testing"
	"time"
)

const timeFormat = "2006-01-02 03:04:05 +0000 UTC"

func TestTimeStamp(t *testing.T) {

	tm, _ := time.Parse(timeFormat, "2017-09-12 08:47:27 +0000 UTC")
	t.Log(tm.Unix())

	tm = time.Unix(1505206047, 0)
	t.Log(tm.Format(timeFormat))

}

func TestSQL(t *testing.T) {
	db, err := sql.Open("mysql",
		"user:password@tcp(127.0.0.1:3306)/hello")
	if err != nil {
		t.Fatal(err)
	}
	defer db.Close()

	rows, err := db.Query("select id, name from users where id = ?", 1)
	if err != nil {
		t.Fatal(err)
	}
	defer rows.Close()


	for rows.Next() {
		err := rows.Scan(&id, &name)
		if err != nil {
			t.Fatal(err)
		}
		t.Log()
	}
}


func TestPmmSQL(t *testing.T) {
	db, err := sql.Open("mysql",
		"pmm:pmm@tcp(10.212.12.36:3306)/pmm")
	if err != nil {
		t.Fatal(err)
	}
	defer db.Close()

	begin, _ := time.Parse(timeFormat, "2017-09-12 08:47:27 +0000 UTC")
	end, _ := time.Parse(timeFormat, "UTC 2017-09-12 09:47:27 +0000 UTC")
	rows, err := db.Query("SELECT query_class_id,"+
		"SUM(query_count), SUM(Query_time_sum), MIN(Query_time_min),"+
		"SUM(Query_time_sum)/SUM(query_count), AVG(Query_time_med),"+
		"AVG(Query_time_p95), MAX(Query_time_max) "+
		"FROM query_class_metrics WHERE instance_id = 66 "+
		"AND (start_ts >= ? AND start_ts < ?) "+
		"GROUP BY query_class_id ORDER BY SUM(Query_time_sum) "+
		"DESC LIMIT 10 OFFSET 0", begin, end)

	if err != nil{
		t.Error(err)
	}

	var queryClassId uint
	t.Log("Begin")
	for rows.Next() {
		t.Log("IN")
		err := rows.Scan(&queryClassId)
		if err != nil {
			t.Error(err)
		}
		t.Log(queryClassId)
	}
}
