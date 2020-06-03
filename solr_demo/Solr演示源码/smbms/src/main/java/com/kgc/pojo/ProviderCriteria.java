package com.kgc.pojo;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class ProviderCriteria {
    protected String orderByClause;

    protected boolean distinct;

    protected List<Criteria> oredCriteria;

    public ProviderCriteria() {
        oredCriteria = new ArrayList<Criteria>();
    }

    public void setOrderByClause(String orderByClause) {
        this.orderByClause = orderByClause;
    }

    public String getOrderByClause() {
        return orderByClause;
    }

    public void setDistinct(boolean distinct) {
        this.distinct = distinct;
    }

    public boolean isDistinct() {
        return distinct;
    }

    public List<Criteria> getOredCriteria() {
        return oredCriteria;
    }

    public void or(Criteria criteria) {
        oredCriteria.add(criteria);
    }

    public Criteria or() {
        Criteria criteria = createCriteriaInternal();
        oredCriteria.add(criteria);
        return criteria;
    }

    public Criteria createCriteria() {
        Criteria criteria = createCriteriaInternal();
        if (oredCriteria.size() == 0) {
            oredCriteria.add(criteria);
        }
        return criteria;
    }

    protected Criteria createCriteriaInternal() {
        Criteria criteria = new Criteria();
        return criteria;
    }

    public void clear() {
        oredCriteria.clear();
        orderByClause = null;
        distinct = false;
    }

    protected abstract static class GeneratedCriteria {
        protected List<Criterion> criteria;

        protected GeneratedCriteria() {
            super();
            criteria = new ArrayList<Criterion>();
        }

        public boolean isValid() {
            return criteria.size() > 0;
        }

        public List<Criterion> getAllCriteria() {
            return criteria;
        }

        public List<Criterion> getCriteria() {
            return criteria;
        }

        protected void addCriterion(String condition) {
            if (condition == null) {
                throw new RuntimeException("Value for condition cannot be null");
            }
            criteria.add(new Criterion(condition));
        }

        protected void addCriterion(String condition, Object value, String property) {
            if (value == null) {
                throw new RuntimeException("Value for " + property + " cannot be null");
            }
            criteria.add(new Criterion(condition, value));
        }

        protected void addCriterion(String condition, Object value1, Object value2, String property) {
            if (value1 == null || value2 == null) {
                throw new RuntimeException("Between values for " + property + " cannot be null");
            }
            criteria.add(new Criterion(condition, value1, value2));
        }

        public Criteria andIdIsNull() {
            addCriterion("id is null");
            return (Criteria) this;
        }

        public Criteria andIdIsNotNull() {
            addCriterion("id is not null");
            return (Criteria) this;
        }

        public Criteria andIdEqualTo(Long value) {
            addCriterion("id =", value, "id");
            return (Criteria) this;
        }

        public Criteria andIdNotEqualTo(Long value) {
            addCriterion("id <>", value, "id");
            return (Criteria) this;
        }

        public Criteria andIdGreaterThan(Long value) {
            addCriterion("id >", value, "id");
            return (Criteria) this;
        }

        public Criteria andIdGreaterThanOrEqualTo(Long value) {
            addCriterion("id >=", value, "id");
            return (Criteria) this;
        }

        public Criteria andIdLessThan(Long value) {
            addCriterion("id <", value, "id");
            return (Criteria) this;
        }

        public Criteria andIdLessThanOrEqualTo(Long value) {
            addCriterion("id <=", value, "id");
            return (Criteria) this;
        }

        public Criteria andIdIn(List<Long> values) {
            addCriterion("id in", values, "id");
            return (Criteria) this;
        }

        public Criteria andIdNotIn(List<Long> values) {
            addCriterion("id not in", values, "id");
            return (Criteria) this;
        }

        public Criteria andIdBetween(Long value1, Long value2) {
            addCriterion("id between", value1, value2, "id");
            return (Criteria) this;
        }

        public Criteria andIdNotBetween(Long value1, Long value2) {
            addCriterion("id not between", value1, value2, "id");
            return (Criteria) this;
        }

        public Criteria andProcodeIsNull() {
            addCriterion("proCode is null");
            return (Criteria) this;
        }

        public Criteria andProcodeIsNotNull() {
            addCriterion("proCode is not null");
            return (Criteria) this;
        }

        public Criteria andProcodeEqualTo(String value) {
            addCriterion("proCode =", value, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeNotEqualTo(String value) {
            addCriterion("proCode <>", value, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeGreaterThan(String value) {
            addCriterion("proCode >", value, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeGreaterThanOrEqualTo(String value) {
            addCriterion("proCode >=", value, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeLessThan(String value) {
            addCriterion("proCode <", value, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeLessThanOrEqualTo(String value) {
            addCriterion("proCode <=", value, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeLike(String value) {
            addCriterion("proCode like", value, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeNotLike(String value) {
            addCriterion("proCode not like", value, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeIn(List<String> values) {
            addCriterion("proCode in", values, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeNotIn(List<String> values) {
            addCriterion("proCode not in", values, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeBetween(String value1, String value2) {
            addCriterion("proCode between", value1, value2, "procode");
            return (Criteria) this;
        }

        public Criteria andProcodeNotBetween(String value1, String value2) {
            addCriterion("proCode not between", value1, value2, "procode");
            return (Criteria) this;
        }

        public Criteria andPronameIsNull() {
            addCriterion("proName is null");
            return (Criteria) this;
        }

        public Criteria andPronameIsNotNull() {
            addCriterion("proName is not null");
            return (Criteria) this;
        }

        public Criteria andPronameEqualTo(String value) {
            addCriterion("proName =", value, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameNotEqualTo(String value) {
            addCriterion("proName <>", value, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameGreaterThan(String value) {
            addCriterion("proName >", value, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameGreaterThanOrEqualTo(String value) {
            addCriterion("proName >=", value, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameLessThan(String value) {
            addCriterion("proName <", value, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameLessThanOrEqualTo(String value) {
            addCriterion("proName <=", value, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameLike(String value) {
            addCriterion("proName like", value, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameNotLike(String value) {
            addCriterion("proName not like", value, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameIn(List<String> values) {
            addCriterion("proName in", values, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameNotIn(List<String> values) {
            addCriterion("proName not in", values, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameBetween(String value1, String value2) {
            addCriterion("proName between", value1, value2, "proname");
            return (Criteria) this;
        }

        public Criteria andPronameNotBetween(String value1, String value2) {
            addCriterion("proName not between", value1, value2, "proname");
            return (Criteria) this;
        }

        public Criteria andProdescIsNull() {
            addCriterion("proDesc is null");
            return (Criteria) this;
        }

        public Criteria andProdescIsNotNull() {
            addCriterion("proDesc is not null");
            return (Criteria) this;
        }

        public Criteria andProdescEqualTo(String value) {
            addCriterion("proDesc =", value, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescNotEqualTo(String value) {
            addCriterion("proDesc <>", value, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescGreaterThan(String value) {
            addCriterion("proDesc >", value, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescGreaterThanOrEqualTo(String value) {
            addCriterion("proDesc >=", value, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescLessThan(String value) {
            addCriterion("proDesc <", value, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescLessThanOrEqualTo(String value) {
            addCriterion("proDesc <=", value, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescLike(String value) {
            addCriterion("proDesc like", value, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescNotLike(String value) {
            addCriterion("proDesc not like", value, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescIn(List<String> values) {
            addCriterion("proDesc in", values, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescNotIn(List<String> values) {
            addCriterion("proDesc not in", values, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescBetween(String value1, String value2) {
            addCriterion("proDesc between", value1, value2, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProdescNotBetween(String value1, String value2) {
            addCriterion("proDesc not between", value1, value2, "prodesc");
            return (Criteria) this;
        }

        public Criteria andProcontactIsNull() {
            addCriterion("proContact is null");
            return (Criteria) this;
        }

        public Criteria andProcontactIsNotNull() {
            addCriterion("proContact is not null");
            return (Criteria) this;
        }

        public Criteria andProcontactEqualTo(String value) {
            addCriterion("proContact =", value, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactNotEqualTo(String value) {
            addCriterion("proContact <>", value, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactGreaterThan(String value) {
            addCriterion("proContact >", value, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactGreaterThanOrEqualTo(String value) {
            addCriterion("proContact >=", value, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactLessThan(String value) {
            addCriterion("proContact <", value, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactLessThanOrEqualTo(String value) {
            addCriterion("proContact <=", value, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactLike(String value) {
            addCriterion("proContact like", value, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactNotLike(String value) {
            addCriterion("proContact not like", value, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactIn(List<String> values) {
            addCriterion("proContact in", values, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactNotIn(List<String> values) {
            addCriterion("proContact not in", values, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactBetween(String value1, String value2) {
            addCriterion("proContact between", value1, value2, "procontact");
            return (Criteria) this;
        }

        public Criteria andProcontactNotBetween(String value1, String value2) {
            addCriterion("proContact not between", value1, value2, "procontact");
            return (Criteria) this;
        }

        public Criteria andProphoneIsNull() {
            addCriterion("proPhone is null");
            return (Criteria) this;
        }

        public Criteria andProphoneIsNotNull() {
            addCriterion("proPhone is not null");
            return (Criteria) this;
        }

        public Criteria andProphoneEqualTo(String value) {
            addCriterion("proPhone =", value, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneNotEqualTo(String value) {
            addCriterion("proPhone <>", value, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneGreaterThan(String value) {
            addCriterion("proPhone >", value, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneGreaterThanOrEqualTo(String value) {
            addCriterion("proPhone >=", value, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneLessThan(String value) {
            addCriterion("proPhone <", value, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneLessThanOrEqualTo(String value) {
            addCriterion("proPhone <=", value, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneLike(String value) {
            addCriterion("proPhone like", value, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneNotLike(String value) {
            addCriterion("proPhone not like", value, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneIn(List<String> values) {
            addCriterion("proPhone in", values, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneNotIn(List<String> values) {
            addCriterion("proPhone not in", values, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneBetween(String value1, String value2) {
            addCriterion("proPhone between", value1, value2, "prophone");
            return (Criteria) this;
        }

        public Criteria andProphoneNotBetween(String value1, String value2) {
            addCriterion("proPhone not between", value1, value2, "prophone");
            return (Criteria) this;
        }

        public Criteria andProaddressIsNull() {
            addCriterion("proAddress is null");
            return (Criteria) this;
        }

        public Criteria andProaddressIsNotNull() {
            addCriterion("proAddress is not null");
            return (Criteria) this;
        }

        public Criteria andProaddressEqualTo(String value) {
            addCriterion("proAddress =", value, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressNotEqualTo(String value) {
            addCriterion("proAddress <>", value, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressGreaterThan(String value) {
            addCriterion("proAddress >", value, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressGreaterThanOrEqualTo(String value) {
            addCriterion("proAddress >=", value, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressLessThan(String value) {
            addCriterion("proAddress <", value, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressLessThanOrEqualTo(String value) {
            addCriterion("proAddress <=", value, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressLike(String value) {
            addCriterion("proAddress like", value, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressNotLike(String value) {
            addCriterion("proAddress not like", value, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressIn(List<String> values) {
            addCriterion("proAddress in", values, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressNotIn(List<String> values) {
            addCriterion("proAddress not in", values, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressBetween(String value1, String value2) {
            addCriterion("proAddress between", value1, value2, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProaddressNotBetween(String value1, String value2) {
            addCriterion("proAddress not between", value1, value2, "proaddress");
            return (Criteria) this;
        }

        public Criteria andProfaxIsNull() {
            addCriterion("proFax is null");
            return (Criteria) this;
        }

        public Criteria andProfaxIsNotNull() {
            addCriterion("proFax is not null");
            return (Criteria) this;
        }

        public Criteria andProfaxEqualTo(String value) {
            addCriterion("proFax =", value, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxNotEqualTo(String value) {
            addCriterion("proFax <>", value, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxGreaterThan(String value) {
            addCriterion("proFax >", value, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxGreaterThanOrEqualTo(String value) {
            addCriterion("proFax >=", value, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxLessThan(String value) {
            addCriterion("proFax <", value, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxLessThanOrEqualTo(String value) {
            addCriterion("proFax <=", value, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxLike(String value) {
            addCriterion("proFax like", value, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxNotLike(String value) {
            addCriterion("proFax not like", value, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxIn(List<String> values) {
            addCriterion("proFax in", values, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxNotIn(List<String> values) {
            addCriterion("proFax not in", values, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxBetween(String value1, String value2) {
            addCriterion("proFax between", value1, value2, "profax");
            return (Criteria) this;
        }

        public Criteria andProfaxNotBetween(String value1, String value2) {
            addCriterion("proFax not between", value1, value2, "profax");
            return (Criteria) this;
        }

        public Criteria andCreatedbyIsNull() {
            addCriterion("createdBy is null");
            return (Criteria) this;
        }

        public Criteria andCreatedbyIsNotNull() {
            addCriterion("createdBy is not null");
            return (Criteria) this;
        }

        public Criteria andCreatedbyEqualTo(Long value) {
            addCriterion("createdBy =", value, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyNotEqualTo(Long value) {
            addCriterion("createdBy <>", value, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyGreaterThan(Long value) {
            addCriterion("createdBy >", value, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyGreaterThanOrEqualTo(Long value) {
            addCriterion("createdBy >=", value, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyLessThan(Long value) {
            addCriterion("createdBy <", value, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyLessThanOrEqualTo(Long value) {
            addCriterion("createdBy <=", value, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyIn(List<Long> values) {
            addCriterion("createdBy in", values, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyNotIn(List<Long> values) {
            addCriterion("createdBy not in", values, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyBetween(Long value1, Long value2) {
            addCriterion("createdBy between", value1, value2, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreatedbyNotBetween(Long value1, Long value2) {
            addCriterion("createdBy not between", value1, value2, "createdby");
            return (Criteria) this;
        }

        public Criteria andCreationdateIsNull() {
            addCriterion("creationDate is null");
            return (Criteria) this;
        }

        public Criteria andCreationdateIsNotNull() {
            addCriterion("creationDate is not null");
            return (Criteria) this;
        }

        public Criteria andCreationdateEqualTo(Date value) {
            addCriterion("creationDate =", value, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateNotEqualTo(Date value) {
            addCriterion("creationDate <>", value, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateGreaterThan(Date value) {
            addCriterion("creationDate >", value, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateGreaterThanOrEqualTo(Date value) {
            addCriterion("creationDate >=", value, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateLessThan(Date value) {
            addCriterion("creationDate <", value, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateLessThanOrEqualTo(Date value) {
            addCriterion("creationDate <=", value, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateIn(List<Date> values) {
            addCriterion("creationDate in", values, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateNotIn(List<Date> values) {
            addCriterion("creationDate not in", values, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateBetween(Date value1, Date value2) {
            addCriterion("creationDate between", value1, value2, "creationdate");
            return (Criteria) this;
        }

        public Criteria andCreationdateNotBetween(Date value1, Date value2) {
            addCriterion("creationDate not between", value1, value2, "creationdate");
            return (Criteria) this;
        }

        public Criteria andModifydateIsNull() {
            addCriterion("modifyDate is null");
            return (Criteria) this;
        }

        public Criteria andModifydateIsNotNull() {
            addCriterion("modifyDate is not null");
            return (Criteria) this;
        }

        public Criteria andModifydateEqualTo(Date value) {
            addCriterion("modifyDate =", value, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateNotEqualTo(Date value) {
            addCriterion("modifyDate <>", value, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateGreaterThan(Date value) {
            addCriterion("modifyDate >", value, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateGreaterThanOrEqualTo(Date value) {
            addCriterion("modifyDate >=", value, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateLessThan(Date value) {
            addCriterion("modifyDate <", value, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateLessThanOrEqualTo(Date value) {
            addCriterion("modifyDate <=", value, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateIn(List<Date> values) {
            addCriterion("modifyDate in", values, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateNotIn(List<Date> values) {
            addCriterion("modifyDate not in", values, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateBetween(Date value1, Date value2) {
            addCriterion("modifyDate between", value1, value2, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifydateNotBetween(Date value1, Date value2) {
            addCriterion("modifyDate not between", value1, value2, "modifydate");
            return (Criteria) this;
        }

        public Criteria andModifybyIsNull() {
            addCriterion("modifyBy is null");
            return (Criteria) this;
        }

        public Criteria andModifybyIsNotNull() {
            addCriterion("modifyBy is not null");
            return (Criteria) this;
        }

        public Criteria andModifybyEqualTo(Long value) {
            addCriterion("modifyBy =", value, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyNotEqualTo(Long value) {
            addCriterion("modifyBy <>", value, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyGreaterThan(Long value) {
            addCriterion("modifyBy >", value, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyGreaterThanOrEqualTo(Long value) {
            addCriterion("modifyBy >=", value, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyLessThan(Long value) {
            addCriterion("modifyBy <", value, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyLessThanOrEqualTo(Long value) {
            addCriterion("modifyBy <=", value, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyIn(List<Long> values) {
            addCriterion("modifyBy in", values, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyNotIn(List<Long> values) {
            addCriterion("modifyBy not in", values, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyBetween(Long value1, Long value2) {
            addCriterion("modifyBy between", value1, value2, "modifyby");
            return (Criteria) this;
        }

        public Criteria andModifybyNotBetween(Long value1, Long value2) {
            addCriterion("modifyBy not between", value1, value2, "modifyby");
            return (Criteria) this;
        }
    }

    public static class Criteria extends GeneratedCriteria {

        protected Criteria() {
            super();
        }
    }

    public static class Criterion {
        private String condition;

        private Object value;

        private Object secondValue;

        private boolean noValue;

        private boolean singleValue;

        private boolean betweenValue;

        private boolean listValue;

        private String typeHandler;

        public String getCondition() {
            return condition;
        }

        public Object getValue() {
            return value;
        }

        public Object getSecondValue() {
            return secondValue;
        }

        public boolean isNoValue() {
            return noValue;
        }

        public boolean isSingleValue() {
            return singleValue;
        }

        public boolean isBetweenValue() {
            return betweenValue;
        }

        public boolean isListValue() {
            return listValue;
        }

        public String getTypeHandler() {
            return typeHandler;
        }

        protected Criterion(String condition) {
            super();
            this.condition = condition;
            this.typeHandler = null;
            this.noValue = true;
        }

        protected Criterion(String condition, Object value, String typeHandler) {
            super();
            this.condition = condition;
            this.value = value;
            this.typeHandler = typeHandler;
            if (value instanceof List<?>) {
                this.listValue = true;
            } else {
                this.singleValue = true;
            }
        }

        protected Criterion(String condition, Object value) {
            this(condition, value, null);
        }

        protected Criterion(String condition, Object value, Object secondValue, String typeHandler) {
            super();
            this.condition = condition;
            this.value = value;
            this.secondValue = secondValue;
            this.typeHandler = typeHandler;
            this.betweenValue = true;
        }

        protected Criterion(String condition, Object value, Object secondValue) {
            this(condition, value, secondValue, null);
        }
    }
}