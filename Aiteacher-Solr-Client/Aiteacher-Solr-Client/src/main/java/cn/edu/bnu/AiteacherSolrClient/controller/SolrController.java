package cn.edu.bnu.AiteacherSolrClient.controller;

import cn.edu.bnu.AiteacherSolrClient.entity.solr.MoralCase;
import cn.edu.bnu.AiteacherSolrClient.service.SolrService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
@RequestMapping(path = "/aiteacher/solr")
public class SolrController {

    @Autowired
    private SolrService solrService;

    /**
     * 根据关键字搜索相关案例
     * @param keywords
     * @param page 分页start index
     * @param size
     * @return
     */
    @RequestMapping(path = "/search/keywords", method = RequestMethod.POST)
    public Map<String, Object> search(@RequestParam(name = "keywords") String keywords,
                                      @RequestParam(name = "page", required = false, defaultValue = "1") int page,
                                      @RequestParam(name = "size", required = false, defaultValue = "30") int size) {
        return solrService.searchByKeywords(keywords, page, size);
    }

    /**
     * 根据案例id查找案例信息
     * */
    @RequestMapping(path = "/search/id", method = RequestMethod.POST)
    public MoralCase searchById(@RequestParam(name = "id") String id) {
        return solrService.searchById(id);
    }

    /**
     * 显示案例详情信息
     * todo 案例位置信息和图片信息
     * */
    @RequestMapping(path = "/search/getcaseinfo", method = RequestMethod.POST)
    public Map<String, Object> getCaseInfoByID(@RequestParam(name = "user_id") String user_id,
                                               @RequestParam(name = "case_id") String case_id,
                                               @RequestParam(name = "viewed", required = false) Boolean viewed) {
        return solrService.getCaseInfo(user_id, case_id, viewed);
    }

}
