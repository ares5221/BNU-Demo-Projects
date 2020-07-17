package cn.edu.bnu.AiteacherSolrClient.repository.solr;

import cn.edu.bnu.AiteacherSolrClient.entity.solr.MoralCase;
import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.SolrQuery.ORDER;
import org.apache.solr.client.solrj.request.FieldAnalysisRequest;
import org.apache.solr.client.solrj.response.AnalysisResponseBase;
import org.apache.solr.client.solrj.response.FieldAnalysisResponse;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocument;
import org.apache.solr.common.SolrDocumentList;
import org.apache.solr.common.params.CursorMarkParams;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.*;

@Component
public class SolrRepository {
    @Autowired
    SolrClient client;

    public MoralCase searchById(String id) {
        MoralCase solrCase = new MoralCase();
        solrCase.setId(id);

        try {
            SolrQuery query = new SolrQuery("ID:" + id)
                    .setStart(0)
                    .setRows(1);

            query.addField("title");
            query.addField("author");
            query.addField("content");

            QueryResponse response = client.query(query);

            SolrDocumentList documents = response.getResults();
            for (SolrDocument document : documents) {
                String title = (String) document.getFirstValue("title");
                solrCase.setTitle(title);
                String author = (String) document.getFirstValue("author");
                solrCase.setAuthor(author);
                String content = (String) document.getFirstValue("content");
                solrCase.setContent(content);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return solrCase;
    }


    /**
     * 给指定的语句分词。
     *
     * @param sentence 被分词的语句
     * @return 分词结果
     */
    public List<String> getAnalysis(String sentence) {
        FieldAnalysisRequest request = new FieldAnalysisRequest(
                "/analysis/field");
        request.addFieldName("title");// 字段名，随便指定一个支持中文分词的字段
        request.setFieldValue("");// 字段值，可以为空字符串，但是需要显式指定此参数
        request.setQuery(sentence);

        FieldAnalysisResponse response = null;
        try {
            response = request.process(client);
        } catch (Exception e) {
            System.out.println("获取查询语句的分词时遇到错误");
        }
        List<String> results = new ArrayList<String>();
        Iterator<AnalysisResponseBase.AnalysisPhase> it = response.getFieldNameAnalysis("title")
                .getQueryPhases().iterator();
        while (it.hasNext()) {
            AnalysisResponseBase.AnalysisPhase pharse = (AnalysisResponseBase.AnalysisPhase) it.next();
            List<AnalysisResponseBase.TokenInfo> list = pharse.getTokens();
            for (AnalysisResponseBase.TokenInfo info : list) {
                results.add(info.getText());
            }

        }
        results = removeDuplicateWithOrder(results);
        return results;
    }

    public List<String> removeDuplicateWithOrder(List<String> list) {
        Set set = new HashSet();
        List newList = new ArrayList();
        for (Iterator iter = list.iterator(); iter.hasNext(); ) {
            Object element = iter.next();
            if (set.add(element))
                newList.add(element);
        }
        list.clear();
        list.addAll(newList);
        System.out.println(" solr 关键字检索去除了重复关键词 " + list);
        return list;
    }

    /**
     * return case title and author
     */
    public List<List<String>> searchByKeywords(String keywords) {
        List<List<String>> items = new ArrayList<>();
        String solr_query = "";
        try {
            if (keywords.equals("*:*")) {
                solr_query = "*:*";
            } else {
                solr_query = "search_keys:" + keywords;
            }
            SolrQuery query = new SolrQuery(solr_query)
                    .addField("ID")
                    .addField("title")
                    .addField("author")
                    .addSort("id", ORDER.asc)
                    .setStart(0)
                    .setRows(500);

            String cursorMark = CursorMarkParams.CURSOR_MARK_START;
            boolean done = false;

            while (!done) {
                query.set(CursorMarkParams.CURSOR_MARK_PARAM, cursorMark);
                QueryResponse response = client.query(query);
                String nextCursorMark = response.getNextCursorMark();
                for (SolrDocument document : response.getResults()) {
                    List<String> item = new ArrayList<>();
                    String ID = (String) document.getFirstValue("ID");
                    item.add(ID);
                    String title = (String) document.getFirstValue("title");
                    item.add(title);
                    String author = (String) document.getFirstValue("author");
                    item.add(author);
                    items.add(item);
                }
                if (cursorMark.equals(nextCursorMark)) {
                    done = true;
                }
                cursorMark = nextCursorMark;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return items;
    }

    public List<List<String>> searchByKeywordsSolr(String keywords,int start, int size) {
        List<List<String>> items = new ArrayList<>();
        String solr_query = "";
        try {
            if (keywords.equals("*:*")) {
                solr_query = "*:*";
            } else {
                solr_query = "search_keys:" + keywords;
            }
            SolrQuery query = new SolrQuery(solr_query)
                    .addField("ID")
                    .addField("title")
                    .addField("author")
                    .addSort("id", ORDER.asc)
                    .setStart(0)
                    .setRows(2000);
//          设置排序规则
            query.set("fl","*,score");
            String cursorMark = CursorMarkParams.CURSOR_MARK_START;
            boolean done = false;

            while (!done) {
                query.set(CursorMarkParams.CURSOR_MARK_PARAM, cursorMark);
                QueryResponse response = client.query(query);
                String nextCursorMark = response.getNextCursorMark();
                int count = 0;
                for (SolrDocument document : response.getResults()) {
                    if(count >=start &&(count <size)){
                        List<String> item = new ArrayList<>();
                        String ID = (String) document.getFirstValue("ID");
                        item.add(ID);
                        String title = (String) document.getFirstValue("title");
                        item.add(title);
                        String author = (String) document.getFirstValue("author");
                        item.add(author);
                        items.add(item);
                    }
                    count +=1;
                }
                if (cursorMark.equals(nextCursorMark)) {
                    done = true;
                }
                cursorMark = nextCursorMark;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return items;
    }

    public List<List<String>> searchByKeywordsBase(String keywords,int start, int size) {
        System.out.println("%%%%%% "+keywords +start +size);
        List<List<String>> items = new ArrayList<>();
        String solr_query = "";
        try {
            if (keywords.equals("*:*")) {
                solr_query = "search_keys:" + "我是一名";
            } else {
                solr_query = "search_keys:" + keywords;
            }
            //2. 执行查询
            //SolrQuery : solr的查询对象
            SolrQuery solrQuery = new SolrQuery(solr_query);
            solrQuery.addField("ID");
            solrQuery.addField("title");
            solrQuery.addField("author");
//            solrQuery.setSort("id", ORDER.desc);
            //设置排序规则
//            solrQuery.set("fl","*,score");
            solrQuery.setStart(start);
            solrQuery.setRows(size);
            QueryResponse response = client.query(solrQuery);

            //3. 获取数据
            SolrDocumentList documentList = response.getResults();
            for (SolrDocument document : documentList) {
                List<String> item = new ArrayList<>();
                String ID = (String) document.get("ID");
                String title = (String) document.get("title");
                String author = (String) document.get("author");
                item.add(ID);
                item.add(title);
                item.add(author);
                System.out.println("%%%%%% "+ID);
                items.add(item);
//                System.out.println("@@@@@@@@@@@ " + items );
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return items;
    }


}
