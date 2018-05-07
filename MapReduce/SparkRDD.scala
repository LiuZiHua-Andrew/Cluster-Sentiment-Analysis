/****
the file is used to do the map reduce in spark

****/
import scala.util.parsing.json.JSON._
import scala.collection.immutable.Map
import scala.io.Source
import org.apache.spark.rdd.RDD
import org.apache.spark.rdd.RDD._
import org.apache.spark.rdd.PairRDDFunctions._
import org.apache.spark.api.java.JavaPairRDD

object SparkRDD {
	def mapreduce(){
		implicit val formats = Serialization.formats(ShortTypeHints(List()));  
		val input = sc.textFile("file:///mnt/database/sparktemp/pared_tweets_for_spark.json");
		val byKey = x.map({case (suburb,drunk) => suburb->count});
		val reducedByKey = byKey.reduceByKey(_ + _);
		reducedByKey.collect.foreach(println);

	}
}