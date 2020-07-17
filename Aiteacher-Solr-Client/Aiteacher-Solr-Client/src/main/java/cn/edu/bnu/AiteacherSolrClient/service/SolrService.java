package cn.edu.bnu.AiteacherSolrClient.service;
import cn.edu.bnu.AiteacherSolrClient.entity.solr.MoralCase;
import cn.edu.bnu.AiteacherSolrClient.repository.solr.SolrRepository;
import cn.edu.bnu.AiteacherSolrClient.util.FilterEmojiUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import java.util.*;

@Service
public class SolrService {

    @Autowired
    private SolrRepository solrRepository;


    public Map<String, Object> searchByKeywords(String keywords, int page, int size) {
        Map<String, Object> map = new HashMap<>();
        List<Map<String, Object>> res = new ArrayList<>();
        keywords = keywords.replaceAll("\\s*", "");

        if (keywords.equals("") || keywords == null) {
            keywords = "*:*";
        }
        if(keywords != null && FilterEmojiUtil.containsEmoji(keywords)){
            System.out.println("输入的检索描述中含有不合法字段emoji符号！");
            map.put("search_list", res);
            map.put("total_count", 0);
            return map;
        }
        int start_index = 0;
        int end_index = 0;
        if (page <=0 ||size <=0){
            start_index = 0;
            end_index = 30;
        }else {
            start_index = (page-1)*size;
            end_index = page*size;
        }
        // 分页机制
        List<List<String>> case_list = solrRepository.searchByKeywordsBase(keywords, start_index, end_index);
        List<List<String>> case_len_info = solrRepository.searchByKeywords(keywords);
        int totalCount = case_len_info.size();
        System.out.println("20200616##" + case_list.size() + case_list);
        List<String> key_list = new ArrayList<String>();
        if (keywords == "*:*") {
            key_list = null;
        } else {
            key_list = solrRepository.getAnalysis(keywords);
        }

//        for (int i = 0; i < case_list.size(); i++) {
//            Map<String, Object> tmp = new HashMap<>();
//            String curr_case_id = case_list.get(i).get(0);
//            String curr_case_title = case_list.get(i).get(1);
//            Integer view_num = caseViewInfoService.findCaseViewNumbyCaseId(curr_case_id);
//            if (view_num == null) {
//                view_num = 0;
//            }
//            String provice_info = "北京市";
//            String pic_path = getCaseImagePath(curr_case_id);
//            tmp.put("case_title", curr_case_title);
//            tmp.put("id", curr_case_id);
//            tmp.put("view_num", view_num);
//            tmp.put("provice_info", provice_info);
//            tmp.put("pic_name", pic_path);
//            tmp.put("key_words_list", key_list);
//            res.add(tmp);
//        }
//        if (keywords.equals("*:*")) {
//            Collections.sort(res, new Comparator<Map<String, Object>>() {
//                @Override
//                public int compare(Map<String, Object> map1, Map<String, Object> map2) {
//                    if (Integer.parseInt(map1.get("view_num").toString()) < Integer.parseInt(map2.get("view_num").toString())) {
//                        return 1;
//                    }
//                    if (Integer.parseInt(map1.get("view_num").toString()) == Integer.parseInt(map2.get("view_num").toString())) {
//                        return 0;
//                    }
//                    return -1;
//                }
//            });
//        }
        map.put("search_list", res);
        map.put("total_count", totalCount);
        return map;
    }


    public String getCaseImagePath(String case_id) {
        int case_id_int = Integer.parseInt(case_id.substring(1, case_id.length()));
        String parentPath = "/public/image/case_image/";
        String image_path = parentPath + "a0000001.jpg";
        if (case_id_int < 70) {
            image_path = parentPath + case_id + ".jpg";
        }else {
            //当前背景图片共有69张,超过69的id 取余循环
            int ran_pic_idx = case_id_int%69;
            image_path = parentPath +"a" + String.format("%07d", ran_pic_idx) + ".jpg";
        }
        return image_path;
    }

    public MoralCase searchById(String id) {
        MoralCase cases = solrRepository.searchById(id);
        return cases;
    }

    public Map<String, Object> getCaseInfo(String user_id, String case_id, Boolean viewed) {
        Map<String, Object> map = new HashMap<>();
        MoralCase case_info = solrRepository.searchById(case_id);
//        Map<String, String> abstuct_info = neo4jService.find_case_information(case_id);
//        boolean is_collect = caseCollectService.checkCollectStatus(user_id, case_id);
//        CaseViewInfo caseViewInfo = caseViewInfoService.findCaseViewInfoByCaseId(case_id);
//        String case_explain = caseExplainService.findCaseExplainByCaseId(case_id);
//        System.out.println("###202000000" + case_explain + case_id);
        long views = 0;
//        if (viewed != null && viewed.booleanValue()) {
//            if (caseViewInfo == null) {
//                CaseViewInfo caseViewInfo2 = new CaseViewInfo();
//                caseViewInfo2.setCase_id(case_id);
//                caseViewInfo2.setView_time(new Date());
//                caseViewInfo2.setViews(1);
//                views = 1;
//                caseViewInfoService.addCaseViewInfo(caseViewInfo2);
//            } else {
//                views = caseViewInfo.getViews() + 1;
//                caseViewInfo.setViews(caseViewInfo.getViews() + 1);
//                caseViewInfoService.updateCaseViewInfoByCaseId(caseViewInfo);
//            }
//        }
        map.put("title", case_info.getTitle());
        map.put("views", views);
        map.put("ID", case_info.getId());
        map.put("content", case_info.getContent());
        map.put("author", case_info.getAuthor());
//        map.put("abstruct_info", abstuct_info);
//        map.put("is_collect", is_collect);
//        map.put("case_explain", case_explain);

        return map;
    }

}
