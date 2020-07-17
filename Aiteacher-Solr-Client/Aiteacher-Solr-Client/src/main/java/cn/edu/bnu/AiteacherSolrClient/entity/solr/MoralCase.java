package cn.edu.bnu.AiteacherSolrClient.entity.solr;

public class MoralCase {
	private String ID;
	private String title;
	private String author;
	private String content;

	public MoralCase() {}
	
	public MoralCase(String id, String title, String author, String content) {
		this.ID= id;
		this.title = title;
		this.author = author;
		this.content = content;
	}

	public String getId() {
		return ID;
	}

	public void setId(String id) {
		this.ID= id;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getAuthor() {
		return author;
	}

	public void setAuthor(String author) {
		this.author = author;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}
}
